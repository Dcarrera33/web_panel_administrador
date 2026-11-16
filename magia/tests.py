"""Pruebas automáticas: python manage.py test"""
import io
import shutil
import tempfile

from django.contrib.auth import get_user_model
from django.core import mail
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from .models import Course, CourseBlock, Faq, GalleryImage, Message, SiteContent, Step

TMP_MEDIA = tempfile.mkdtemp()


def png(w=40, h=30):
    from PIL import Image
    buf = io.BytesIO()
    Image.new("RGB", (w, h), (30, 80, 60)).save(buf, "PNG")
    return buf.getvalue()


@override_settings(EMAIL_ASYNC=False, EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
                   NOTIFY_EMAIL="dueno@example.com", RATE_LIMIT_ENABLED=False, MEDIA_ROOT=TMP_MEDIA)
class PublicTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TMP_MEDIA, ignore_errors=True)

    def setUp(self):
        cache.clear()
        self.course = Course.objects.create(title="Cartomagia básica", summary="Cartas desde cero", description="Hola\n\nMundo",
                                            price_text="99 €", level="principiante", duration="4 sesiones")
        CourseBlock.objects.create(course=self.course, title="Qué aprenderás", text="- Pase\n- Corte", order=1)
        CourseBlock.objects.create(course=self.course, title="Requisitos", text="Una baraja.", order=2)

    def test_pages_render(self):
        for url in ("/", "/cursos/", f"/cursos/{self.course.slug}/", "/saber-mas/", "/contacto/", "/contacto/enviado/",
                    "/legal/aviso-legal/", "/legal/privacidad/", "/legal/cookies/", "/theme.css"):
            self.assertEqual(self.client.get(url).status_code, 200, url)
        self.assertEqual(self.client.get("/legal/nada/").status_code, 404)
        self.assertEqual(self.client.get("/cursos/no-existe/").status_code, 404)

    def test_double_header_and_menu(self):
        html = self.client.get("/").content.decode()
        self.assertIn("Magia en el bosque", html)
        for label in ("Inicio", "Cursos", "Saber más", "Contacto"):
            self.assertIn(f">{label}</a>", html)
        self.assertIn("instagram", html.lower())

    def test_home_split_uses_site_content(self):
        s = SiteContent.load()
        s.home_title = "Soy Alex, mago"
        s.home_text = "Primer párrafo.\n\nSegundo párrafo."
        s.save()
        html = self.client.get("/").content.decode()
        self.assertIn("Soy Alex, mago", html)
        self.assertIn("Primer párrafo.", html)
        self.assertIn("Segundo párrafo.", html)

    def test_home_photo_is_shown_and_optimised(self):
        s = SiteContent.load()
        s.home_photo = SimpleUploadedFile("foto.png", png(2400, 3000), content_type="image/png")
        s.save()
        self.assertTrue(s.home_photo.name.endswith(".jpg"))
        self.assertLessEqual(max(s.home_photo.width, s.home_photo.height), 1400)
        self.assertIn(s.home_photo.url, self.client.get("/").content.decode())

    def test_course_list_shows_name_and_short_description_only(self):
        html = self.client.get("/cursos/").content.decode()
        self.assertIn("Cartomagia básica", html)
        self.assertIn("Cartas desde cero", html)
        self.assertNotIn("Qué aprenderás", html)   # el detalle solo se ve dentro del curso

    def test_course_detail_has_blocks_and_contact_link(self):
        html = self.client.get(f"/cursos/{self.course.slug}/").content.decode()
        self.assertIn("Qué aprenderás", html)
        self.assertIn("<li>Pase</li>", html)
        self.assertIn("Una baraja.", html)
        self.assertIn("99 €", html)
        self.assertIn(f"/contacto/?curso={self.course.slug}", html)

    def test_hidden_course_is_not_public(self):
        Course.objects.filter(pk=self.course.pk).update(active=False)
        self.assertNotIn("Cartomagia básica", self.client.get("/cursos/").content.decode())
        self.assertEqual(self.client.get(f"/cursos/{self.course.slug}/").status_code, 404)

    def test_course_without_price_says_consult(self):
        Course.objects.filter(pk=self.course.pk).update(price_text="")
        self.assertIn("Consultar precio", self.client.get(f"/cursos/{self.course.slug}/").content.decode())

    def test_slug_is_unique(self):
        c2 = Course.objects.create(title="Cartomagia básica", summary="otro")
        self.assertNotEqual(c2.slug, self.course.slug)

    def test_saber_mas_has_carousel_steps_faq(self):
        for i in range(3):
            GalleryImage.objects.create(image=SimpleUploadedFile(f"g{i}.png", png(1600, 900), content_type="image/png"), caption=f"Foto {i}", order=i)
        Step.objects.create(title="Paso uno", text="Explicación uno")
        Faq.objects.create(question="¿Pregunta?", answer="Respuesta.")
        html = self.client.get("/saber-mas/").content.decode()
        self.assertIn("data-carousel", html)
        self.assertEqual(html.count('<figure class="carousel__slide'), 3)
        self.assertEqual(html.count('aria-label="Ir a la foto'), 3)
        self.assertIn("Paso uno", html)
        self.assertIn("¿Pregunta?", html)

    def test_single_photo_has_no_controls(self):
        GalleryImage.objects.create(image=SimpleUploadedFile("g.png", png(1600, 900), content_type="image/png"))
        html = self.client.get("/saber-mas/").content.decode()
        self.assertNotIn("carousel__btn", html)

    def test_inactive_gallery_items_hidden(self):
        GalleryImage.objects.create(image=SimpleUploadedFile("g.png", png(1600, 900), content_type="image/png"), active=False)
        self.assertNotIn("data-carousel", self.client.get("/saber-mas/").content.decode())

    # ---------------- contacto ----------------
    def _send(self, **extra):
        data = dict(name="Ana Pérez", email="ana@example.com", message="Hola, quiero info", consent="1", course="")
        data.update(extra)
        return self.client.post("/contacto/", data)

    def test_contact_saves_message_and_sends_email(self):
        r = self._send(course="Cartomagia básica")
        self.assertRedirects(r, "/contacto/enviado/")
        m = Message.objects.get()
        self.assertEqual((m.name, m.email, m.course, m.is_read), ("Ana Pérez", "ana@example.com", "Cartomagia básica", False))
        self.assertEqual(len(mail.outbox), 1)
        out = mail.outbox[0]
        self.assertEqual(out.to, ["dueno@example.com"])
        self.assertEqual(out.reply_to, ["ana@example.com"])
        self.assertIn("Cartomagia básica", out.subject)
        self.assertIn("Hola, quiero info", out.body)

    def test_contact_validations(self):
        for data, text in [(dict(name=""), "Escribe tu nombre"), (dict(email="no-es-email"), "correo válido"),
                           (dict(message="  "), "Escribe tu mensaje"), (dict(consent=""), "política de privacidad")]:
            r = self._send(**data)
            self.assertEqual(r.status_code, 200)
            self.assertIn(text, r.content.decode())
        self.assertEqual(Message.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_contact_honeypot_and_unknown_course(self):
        self._send(hp_zq7="spam")
        self.assertEqual(Message.objects.count(), 0)
        self._send(course="Curso inventado")
        self.assertEqual(Message.objects.get().course, "")

    def test_contact_header_injection_is_neutralised(self):
        self._send(name="Ana\r\nBcc: x@evil.com")
        self.assertEqual(len(mail.outbox), 1)
        self.assertNotIn("\n", mail.outbox[0].subject)
        self.assertEqual(mail.outbox[0].bcc, [])

    def test_contact_prefills_course(self):
        html = self.client.get(f"/contacto/?curso={self.course.slug}").content.decode()
        self.assertIn('value="Cartomagia básica" selected', html)

    @override_settings(RATE_LIMIT_ENABLED=True)
    def test_contact_rate_limit(self):
        codes = [self._send().status_code for _ in range(6)]
        self.assertEqual(codes[:4], [302] * 4)
        self.assertEqual(codes[-1], 429)

    def test_csrf_enforced(self):
        from django.test import Client
        c = Client(enforce_csrf_checks=True)
        self.assertEqual(c.post("/contacto/", dict(name="x")).status_code, 403)

    def test_security_headers(self):
        r = self.client.get("/")
        self.assertIn("default-src 'self'", r["Content-Security-Policy"])
        self.assertNotIn("style=", r.content.decode())  # la política bloquea estilos en línea

    def test_legal_pages_use_panel_data_and_never_crash(self):
        html = self.client.get("/legal/privacidad/").content.decode()
        self.assertIn("[OWNER]", html)               # sin datos, se ve el hueco
        s = SiteContent.load()
        s.legal_owner, s.legal_cif, s.legal_email = "Alex Mago S.L.", "B12345678", "alex@example.com"
        s.save()
        html = self.client.get("/legal/privacidad/").content.decode()
        self.assertIn("Alex Mago S.L.", html)
        self.assertIn("B12345678", html)
        self.assertNotIn("{", html.replace("{{", ""))
        self.assertIn("csrftoken", self.client.get("/legal/cookies/").content.decode())

    def test_colors_from_panel_in_theme(self):
        s = SiteContent.load()
        s.color_accent = "#ff00aa"
        s.save()
        self.assertIn("--c-accent:#ff00aa", self.client.get("/theme.css").content.decode())

    def test_error_pages(self):
        self.assertIn("No hemos encontrado", self.client.get("/no-existe/").content.decode())


@override_settings(EMAIL_ASYNC=False, EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend", MEDIA_ROOT=TMP_MEDIA)
class AdminTests(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser("dueno", "d@example.com", "una-clave-larga-123")
        self.client.force_login(self.admin)

    def test_requires_login(self):
        self.client.logout()
        self.assertEqual(self.client.get("/gestion/").status_code, 302)

    def test_dashboard_shows_unread_and_latest(self):
        Message.objects.create(name="Luis", email="l@example.com", message="Una duda sobre el curso")
        html = self.client.get("/gestion/").content.decode()
        self.assertIn("Luis", html)
        self.assertIn("NUEVO", html)
        self.assertIn("Todo el panel", html)

    def test_site_content_is_a_single_editable_page(self):
        r = self.client.get("/gestion/magia/sitecontent/")
        self.assertRedirects(r, "/gestion/magia/sitecontent/1/change/")
        self.assertEqual(self.client.get("/gestion/magia/sitecontent/add/").status_code, 403)
        data = {f.name: getattr(SiteContent.load(), f.name) for f in SiteContent._meta.fields
                if f.name not in ("id", "home_photo")}
        data.update(home_title="Nuevo título", home_photo="")
        r = self.client.post("/gestion/magia/sitecontent/1/change/", data)
        self.assertEqual(r.status_code, 302)
        self.assertEqual(SiteContent.objects.count(), 1)
        self.assertEqual(SiteContent.load().home_title, "Nuevo título")
        self.assertIn("Nuevo título", self.client.get("/").content.decode())

    def test_message_is_marked_read_when_opened(self):
        m = Message.objects.create(name="Luis", email="l@example.com", message="Hola")
        self.assertEqual(self.client.get(f"/gestion/magia/message/{m.pk}/change/").status_code, 200)
        m.refresh_from_db()
        self.assertTrue(m.is_read)
        self.assertEqual(self.client.get("/gestion/magia/message/add/").status_code, 403)

    def test_create_course_with_blocks_from_panel(self):
        r = self.client.post("/gestion/magia/course/add/", {
            "title": "Mentalismo", "summary": "Leer mentes", "description": "", "level": "intermedio", "duration": "", "modality": "",
            "price_text": "", "order": 1, "active": "on",
            "blocks-TOTAL_FORMS": 1, "blocks-INITIAL_FORMS": 0, "blocks-MIN_NUM_FORMS": 0, "blocks-MAX_NUM_FORMS": 1000,
            "blocks-0-title": "Temario", "blocks-0-text": "- Uno\n- Dos", "blocks-0-order": 1,
        })
        self.assertEqual(r.status_code, 302, getattr(r, "context_data", None))
        c = Course.objects.get(title="Mentalismo")
        self.assertEqual(c.blocks.count(), 1)
        self.assertIn("<li>Uno</li>", self.client.get(f"/cursos/{c.slug}/").content.decode())

    def test_all_models_have_admin_pages(self):
        for name in ("sitecontent", "course", "galleryimage", "step", "faq", "message"):
            self.assertEqual(self.client.get(f"/gestion/magia/{name}/", follow=True).status_code, 200, name)

    def test_seed_demo(self):
        from django.core.management import call_command
        call_command("seed_demo", stdout=io.StringIO())
        self.assertGreaterEqual(Course.objects.count(), 3)
        self.assertGreaterEqual(GalleryImage.objects.count(), 3)
        self.assertTrue(SiteContent.load().home_photo)
        out = io.StringIO()
        call_command("seed_demo", stdout=out)
        self.assertIn("Ya hay cursos", out.getvalue())


class RichTextTests(TestCase):
    def test_windows_line_breaks_and_paragraphs(self):
        from magia.text import render_text
        html = render_text("Primer párrafo.\r\n\r\nSegundo párrafo\r\ncon salto.")
        self.assertEqual(html.count("<p>"), 2)
        self.assertIn("Segundo párrafo<br>con salto.", html)

    def test_mixed_text_and_bullets(self):
        from magia.text import render_text
        html = render_text("Aprenderás:\n- Forzaje\n- Doble corte\n\nY además mucho más.")
        self.assertEqual(html.count("<ul"), 1)
        self.assertEqual(html.count("<li>"), 2)
        self.assertEqual(html.count("<p>"), 2)
        self.assertLess(html.index("Aprenderás"), html.index("<ul"))
        self.assertLess(html.index("</ul>"), html.index("Y además"))

    def test_escapes_html_and_empty(self):
        from magia.text import render_text
        self.assertIn("&lt;b&gt;", render_text("<b>x</b>"))
        self.assertEqual(render_text(""), "")

    def test_course_page_renders_blocks(self):
        c = Course.objects.create(title="T", summary="s", description="A\r\n\r\nB")
        c.blocks.create(title="Temario", text="Intro\r\n- uno\r\n- dos", order=1)
        r = self.client.get(f"/cursos/{c.slug}/")
        self.assertContains(r, "<li>uno</li>")
        self.assertContains(r, "<p>Intro</p>")
        self.assertContains(r, "<p>B</p>")


class MissingPhotoTests(TestCase):
    def test_saving_with_missing_photo_file_does_not_crash(self):
        from .models import validate_image_size
        site = SiteContent.load()
        SiteContent.objects.filter(pk=1).update(home_photo="inicio/no-existe.jpg")
        site.refresh_from_db()
        validate_image_size(site.home_photo)  # no debe lanzar FileNotFoundError
