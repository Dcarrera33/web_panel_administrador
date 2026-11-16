"""Las páginas de la web."""
import logging
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET

from . import emails
from .legal_texts import LEGAL
from .models import Course, Faq, GalleryImage, Message, SiteContent, Step
from .ratelimit import rate_limit

FONTS = {"title": "Cormorant Garamond", "script": "Pinyon Script", "body": "DM Sans"}
FONT_FALLBACKS = {
    "title": "Georgia, 'Times New Roman', serif",
    "script": "'Brush Script MT', cursive",
    "body": "system-ui, -apple-system, 'Segoe UI', Roboto, Arial, sans-serif",
}


@require_GET
@cache_control(max_age=30, public=True)  # corto: así un cambio de color en el panel se ve enseguida
def theme_css(request):
    """Colores (editables en el panel) y tipografías de la web."""
    s = SiteContent.load()
    font_vars = "".join(f"--font-{role}:'{FONTS[role]}',{FONT_FALLBACKS[role]};" for role in FONTS)
    css = (
        ":root{"
        f"--c-dark:{s.color_dark};--c-primary:{s.color_primary};--c-accent:{s.color_accent};--c-magic:{s.color_magic};--c-light:#efeadc;--c-surface:#f3eee2;--c-ink:#15231c;"
        f"{font_vars}"
        "}"
    )
    return HttpResponse(css, content_type="text/css")


def index(request):
    return render(request, "magia/index.html", {"courses": Course.objects.filter(active=True)[:3]})


def cursos(request):
    return render(request, "magia/cursos.html", {"courses": Course.objects.filter(active=True)})


def curso_detalle(request, slug):
    course = get_object_or_404(Course.objects.prefetch_related("blocks"), slug=slug, active=True)
    return render(request, "magia/curso.html", {"course": course})


def saber_mas(request):
    return render(request, "magia/saber_mas.html", {
        "gallery": GalleryImage.objects.filter(active=True),
        "steps": Step.objects.filter(active=True),
        "faqs": Faq.objects.filter(active=True),
    })


# --------------------------------------------------------------------------
# Contacto
# --------------------------------------------------------------------------
def _parse_contact(form, valid_courses):
    errors = {}
    name = " ".join(form.get("name", "").split())[:100]
    email = form.get("email", "").strip()
    message = form.get("message", "").strip()[:2000]
    course = form.get("course", "").strip()
    if not name:
        errors["name"] = "Escribe tu nombre."
    try:
        validate_email(email)
        if len(email) > 254:
            raise ValidationError("largo")
    except ValidationError:
        errors["email"] = "Escribe un correo válido."
    if not message:
        errors["message"] = "Escribe tu mensaje."
    if not form.get("consent"):
        errors["consent"] = "Debes aceptar la política de privacidad."
    if course not in valid_courses:
        course = ""
    return dict(name=name, email=email, message=message, course=course), errors


@rate_limit("contacto", [(4, 60), (20, 86400)])
def contacto(request):
    site = SiteContent.load()
    titles = list(Course.objects.filter(active=True).values_list("title", flat=True))
    errors, form = {}, {}
    if request.method == "POST":
        form = request.POST
        if form.get("hp_zq7"):  # campo trampa (honeypot): solo lo rellenan los robots
            logging.getLogger("contacto").warning("Mensaje descartado por el campo trampa (posible robot).")
            return redirect("contacto_ok")
        data, errors = _parse_contact(form, titles)
        if not errors:
            msg = Message.objects.create(**data)
            emails.notify_message(msg, site)
            return redirect("contacto_ok")
    else:
        wanted = request.GET.get("curso", "")
        course = Course.objects.filter(slug=wanted, active=True).first()
        if course:
            form = {"course": course.title}
    return render(request, "magia/contacto.html", {"form": form, "errors": errors, "course_titles": titles})


def contacto_ok(request):
    return render(request, "magia/contacto_ok.html")


# --------------------------------------------------------------------------
# Páginas legales
# --------------------------------------------------------------------------
class _Fields(dict):  # si falta algún dato legal, se muestra [CAMPO] en vez de dar error
    def __missing__(self, key):
        return f"[{key.upper()}]"


def legal(request, page):
    data = LEGAL.get(page)
    if not data:
        raise Http404
    s = SiteContent.load()
    fields = _Fields({
        "owner": s.legal_owner or None, "cif": s.legal_cif or None, "address": s.legal_address or None,
        "phone": s.legal_phone or None, "email": s.legal_email or s.contact_email or None,
        "hosting": s.legal_hosting or None, "retention": s.legal_retention or None,
        "updated": s.legal_updated or None,
    })
    fields = _Fields({k: v for k, v in fields.items() if v})
    blocks = []  # [("h2", texto) | ("p", texto) | ("ul", [items])]
    for raw in data["paragraphs"]:
        text = raw.format_map(fields)
        if text.startswith("## "):
            blocks.append(("h2", text[3:]))
        elif text.startswith("- "):
            if blocks and blocks[-1][0] == "ul":
                blocks[-1][1].append(text[2:])
            else:
                blocks.append(("ul", [text[2:]]))
        else:
            blocks.append(("p", text))
    return render(request, "magia/legal.html", {"page": page, "title": data["title"], "blocks": blocks})


# --------------------------------------------------------------------------
# Errores
# --------------------------------------------------------------------------
def _error(request, code, message=""):
    return render(request, "magia/error.html", {"code": code, "message": message}, status=code)


def error_404(request, exception=None):
    return _error(request, 404, "No hemos encontrado esa página.")


def error_403(request, exception=None):
    return _error(request, 403, "No tienes permiso para ver esto.")


def error_500(request):
    return _error(request, 500, "Algo ha fallado. Inténtalo de nuevo en unos minutos.")
