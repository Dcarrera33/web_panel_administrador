"""Carga contenido de EJEMPLO para ver la web llena: python manage.py seed_demo [--force]

Crea cursos, pasos, preguntas, fotos del carrusel (dibujos de bosque generados al vuelo) y una
foto de inicio. Todo se sustituye después desde el panel /gestion/.
"""
import io
import random

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from magia.models import Course, CourseBlock, Faq, GalleryImage, SiteContent, Step


def forest_scene(w, h, seed, tint=(40, 90, 70), moon=True):
    """Dibuja un bosque nocturno (cielo degradado, estrellas, luna y pinos)."""
    from PIL import Image, ImageDraw, ImageFilter

    rnd = random.Random(seed)
    img = Image.new("RGB", (w, h))
    px = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        c = (int(12 + tint[0] * t * 0.5), int(16 + tint[1] * t * 0.6), int(34 + tint[2] * t * 0.35))
        px.line([(0, y), (w, y)], fill=c)
    glow = Image.new("RGB", (w, h), (0, 0, 0))
    g = ImageDraw.Draw(glow)
    mx, my, mr = int(w * rnd.uniform(.55, .8)), int(h * rnd.uniform(.18, .3)), int(min(w, h) * .09)
    for _ in range(90):
        g.point((rnd.randint(0, w), rnd.randint(0, int(h * .55))), fill=(230, 220, 190))
    if moon:
        g.ellipse((mx - mr * 3, my - mr * 3, mx + mr * 3, my + mr * 3), fill=(40, 34, 70))
    glow = glow.filter(ImageFilter.GaussianBlur(mr))
    from PIL import ImageChops
    img = ImageChops.add(img, glow)
    d = ImageDraw.Draw(img)
    for _ in range(70):
        x, y = rnd.randint(0, w), rnd.randint(0, int(h * .55))
        d.ellipse((x, y, x + 2, y + 2), fill=(240, 232, 205))
    if moon:
        d.ellipse((mx - mr, my - mr, mx + mr, my + mr), fill=(244, 232, 190))
        d.ellipse((mx - mr + mr // 3, my - mr - mr // 6, mx + mr + mr // 3, my + mr - mr // 6), fill=(30, 26, 60))
        d.ellipse((mx - mr, my - mr, mx + mr, my + mr), outline=(244, 232, 190), width=2)
    for layer, (shade, count, scale) in enumerate([((14, 36, 30), 14, .55), ((8, 24, 20), 18, .75), ((4, 12, 10), 22, 1.0)]):
        for _ in range(count):
            tw = int(w * rnd.uniform(.07, .13) * (1 + layer * .2))
            th = int(h * rnd.uniform(.28, .5) * scale)
            cx = rnd.randint(-tw // 2, w + tw // 2)
            base = h + 5
            for tier in range(4):
                top = base - th * (tier + 1) // 4
                spread = tw // 2 * (1 - tier * .22)
                d.polygon([(cx - spread, base - th * tier // 4), (cx, top), (cx + spread, base - th * tier // 4)], fill=shade)
            d.rectangle((cx - 3, base - 6, cx + 3, h), fill=shade)
    fog = Image.new("RGB", (w, h), (0, 0, 0))
    ImageDraw.Draw(fog).rectangle((0, int(h * .72), w, h), fill=(30, 50, 56))
    img = ImageChops.add(img, fog.filter(ImageFilter.GaussianBlur(h * .08)))
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=84)
    return ContentFile(buf.getvalue())


COURSES = [
    dict(title="Magia de cerca para empezar", level="principiante", duration="6 sesiones de 90 min", modality="Online en directo",
         price_text="120 €", summary="Tus primeros trucos con cartas, monedas y objetos cotidianos, explicados paso a paso.",
         description="Un curso pensado para quien nunca ha hecho magia. Empezamos por lo básico —cómo sostener las cartas, cómo "
                     "mirar, cómo hablar— y terminamos con una pequeña rutina completa para enseñar a tus amigos.\n\n"
                     "No hace falta tener habilidad previa: solo ganas de practicar un poco cada día.",
         blocks=[("Qué aprenderás", "- Seis efectos con cartas, monedas y gomas elásticas\n- La técnica de manos que hay detrás de cada uno\n"
                                    "- Cómo atraer la atención y dirigir la mirada\n- Una rutina completa de cinco minutos"),
                 ("Qué necesitas", "- Una baraja de cartas francesa\n- Cuatro monedas iguales\n- Un espejo o la cámara del móvil para practicar"),
                 ("A quién va dirigido", "A cualquier persona mayor de 12 años que quiera aprender magia desde cero, sin experiencia previa.")]),
    dict(title="Cartomagia avanzada", level="avanzado", duration="8 sesiones de 2 h", modality="Presencial en Madrid",
         price_text="240 €", summary="Controles, forzajes y falsos cortes: técnica seria para quien ya domina lo básico.",
         description="Para magos con algo de práctica que quieren llevar sus manos al siguiente nivel.\n\n"
                     "Trabajamos la técnica en grupo reducido, con corrección personalizada en cada sesión.",
         blocks=[("Temario", "- Controles y pases clásicos\n- Forzajes invisibles\n- Falsos cortes y barajados\n- Construcción de una rutina de escenario"),
                 ("Requisitos", "Dominar los movimientos básicos con cartas (pase, corte, barajado). Si dudas, escríbeme y lo vemos.")]),
    dict(title="Mentalismo y psicología", level="intermedio", duration="5 sesiones de 90 min", modality="Online en directo",
         price_text="", summary="El arte de leer a la gente y crear la ilusión de adivinar lo que piensa.",
         description="Aprende los principios del mentalismo: sugestión, lectura de lenguaje corporal y presentaciones que dejan sin palabras.",
         blocks=[("Qué aprenderás", "- Principios de sugestión y de psicología\n- Cinco efectos sin material especial\n- Cómo presentar un efecto con tu propia personalidad")]),
    dict(title="Magia para familias", level="todos", duration="1 sesión de 2 h", modality="Presencial",
         price_text="35 € por familia", summary="Una tarde para aprender juntos trucos sencillos y divertidos, de peques a abuelos.",
         description="Un taller corto, cercano y muy divertido para disfrutar en familia.", blocks=[]),
]
STEPS = [
    ("Elige tu curso", "Mira los cursos, lee el temario de cada uno y escríbeme si tienes dudas. Te ayudo a elegir el que mejor encaja contigo."),
    ("Reserva tu plaza", "Me escribes por el formulario o por Instagram y acordamos fechas, forma de pago y modalidad."),
    ("Aprende y practica", "Sesiones guiadas, con ejercicios entre una clase y otra. Puedes preguntarme todo lo que necesites."),
    ("Actúa delante de otros", "Al final del curso preparamos una pequeña actuación para que pierdas el miedo a enseñar lo que has aprendido."),
]
FAQS = [
    ("¿Necesito experiencia previa?", "Solo en los cursos de nivel intermedio y avanzado. Los de principiante empiezan desde cero."),
    ("¿Cuánto material tengo que comprar?", "Muy poco: en cada curso te indico qué necesitas, casi siempre una baraja y objetos que ya tienes en casa."),
    ("¿Puedo hacer un curso online si vivo lejos?", "Sí, los cursos online se imparten en directo por videollamada, y puedes preguntar y recibir correcciones al momento."),
    ("¿Qué pasa si no puedo asistir a una sesión?", "Escríbeme con antelación y buscamos otro día o te paso el material para que no te pierdas nada."),
]


class Command(BaseCommand):
    help = "Carga cursos, pasos, preguntas y fotos de ejemplo."

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Borra los cursos y el carrusel actuales y los vuelve a crear.")

    def handle(self, *args, **opts):
        if Course.objects.exists() and not opts["force"]:
            self.stdout.write("Ya hay cursos. Usa --force para volver a cargar el ejemplo (borra los actuales).")
            return
        if opts["force"]:
            Course.objects.all().delete(); GalleryImage.objects.all().delete(); Step.objects.all().delete(); Faq.objects.all().delete()

        site = SiteContent.load()
        if not site.home_photo:
            site.home_photo.save("inicio-demo.jpg", forest_scene(900, 1125, 1, moon=True), save=False)
            site.save()

        tints = [(40, 90, 70), (60, 60, 110), (90, 70, 50), (40, 80, 100)]
        for i, c in enumerate(COURSES):
            data = dict(c)
            blocks = data.pop("blocks")
            course = Course(order=i + 1, **data)
            course.image.save(f"curso-{i + 1}.jpg", forest_scene(1000, 625, 10 + i, tints[i % 4]), save=False)
            course.save()
            for j, (title, text) in enumerate(blocks):
                CourseBlock.objects.create(course=course, title=title, text=text, order=j + 1)

        captions = ["Una clase en pleno bosque", "Cartas, monedas y mucha práctica", "Cada actuación cuenta una historia", "Aprender mirando de cerca"]
        for i, cap in enumerate(captions):
            g = GalleryImage(caption=cap, order=i + 1)
            g.image.save(f"carrusel-{i + 1}.jpg", forest_scene(1600, 900, 40 + i, tints[i % 4], moon=i % 2 == 0), save=False)
            g.save()

        for i, (t, x) in enumerate(STEPS):
            Step.objects.create(title=t, text=x, order=i + 1)
        for i, (q, a) in enumerate(FAQS):
            Faq.objects.create(question=q, answer=a, order=i + 1)
        self.stdout.write(self.style.SUCCESS("Contenido de ejemplo cargado."))
