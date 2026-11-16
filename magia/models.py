"""Tablas de la base de datos (MySQL).

Cada clase = una tabla. Cada campo (models.XxxField) = una columna.
Después de cambiar algo aquí: python manage.py makemigrations && python manage.py migrate
"""
import io
import os

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.validators import RegexValidator
from django.db import models
from django.utils.text import slugify

HEX_COLOR = RegexValidator(r"^#[0-9a-fA-F]{6}$", "Escribe un color como #1a3a2c.")
MAX_IMAGE_MB = 8


def validate_image_size(f):
    try:
        size = f.size if f else 0
    except OSError:  # la foto guardada ya no está en disco: no impedir guardar el resto
        return
    if size > MAX_IMAGE_MB * 1024 * 1024:
        raise ValidationError(f"La foto pesa demasiado (máximo {MAX_IMAGE_MB} MB).")


def optimize_image(field_file, max_side=1600):
    """Si se acaba de subir una foto: la gira bien, la reduce y la guarda como JPG ligero
    (así las fotos del móvil no ralentizan la web)."""
    from PIL import Image, ImageOps

    if not field_file or getattr(field_file, "_committed", True):
        return
    img = ImageOps.exif_transpose(Image.open(field_file))
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1])
        img = background
    else:
        img = img.convert("RGB")
    img.thumbnail((max_side, max_side))
    buffer = io.BytesIO()
    img.save(buffer, "JPEG", quality=85, optimize=True)
    base = os.path.splitext(os.path.basename(field_file.name))[0]
    field_file.save(f"{base}.jpg", ContentFile(buffer.getvalue()), save=False)


# ============================================================================
# TEXTOS Y DATOS DE TODA LA WEB (una sola ficha, se edita desde el panel)
# ============================================================================
class SiteContent(models.Model):
    # --- Cabecera y pie ---
    site_name = models.CharField("Nombre de la web (cabecera)", max_length=80, default="Magia en el bosque")
    tagline = models.CharField("Frase corta (descripción para Google)", max_length=160,
                               default="Cursos de magia con una mirada distinta: cartomagia, magia de cerca y mentalismo.")
    footer_text = models.CharField("Texto del pie de página", max_length=200, blank=True,
                                   default="Cursos de magia · Aprende, practica y sorprende.")

    # --- Inicio (foto a la izquierda, texto a la derecha) ---
    home_photo = models.ImageField("Foto de inicio", upload_to="inicio/", blank=True,
                                   validators=[validate_image_size],
                                   help_text="Se muestra a la izquierda. Mejor vertical o cuadrada (unos 900×1100 px).")
    home_kicker = models.CharField("Frase pequeña de arriba", max_length=60, blank=True, default="Bienvenido al bosque")
    home_title = models.CharField("Título", max_length=120, default="Aprende magia de verdad")
    home_text = models.TextField("Texto de presentación", blank=True,
                                 default="Soy [tu nombre], mago y profesor. Llevo años actuando y enseñando, y creo que la magia "
                                         "se aprende mejor sin prisa, con buenas manos y una buena historia.\n\n"
                                         "Aquí encontrarás mis cursos: desde los primeros trucos hasta rutinas completas para "
                                         "actuar delante de la gente. Cuéntame qué te gustaría aprender y te ayudo a elegir.",
                                 help_text="Línea en blanco = párrafo nuevo. Líneas que empiezan por «- » = lista.")
    home_signature = models.CharField("Firma", max_length=60, blank=True, default="[Tu nombre]")
    home_button_text = models.CharField("Texto del botón", max_length=40, default="Ver los cursos")

    # --- Saber más ---
    about_title = models.CharField("Título de «Saber más»", max_length=100, default="Cómo funcionan los cursos")
    about_intro = models.TextField("Texto de introducción", blank=True,
                                   default="Cada curso está pensado para que aprendas a tu ritmo, con explicaciones claras, "
                                           "práctica guiada y la posibilidad de preguntar todas tus dudas.")

    # --- Contacto ---
    contact_intro = models.TextField("Texto de la página de contacto", blank=True,
                                     default="¿Tienes dudas sobre algún curso o quieres saber cuál te conviene? Escríbeme y "
                                             "te respondo lo antes posible.")
    contact_email = models.EmailField("Correo que se muestra en la web", blank=True)
    instagram_handle = models.CharField("Usuario de Instagram (sin @)", max_length=60, blank=True, default="magiaenelbosque")
    instagram_url = models.URLField("Enlace de Instagram", blank=True, default="https://instagram.com/")

    # --- Colores (opcional) ---
    color_dark = models.CharField("Color oscuro (cabecera superior y pie)", max_length=7, default="#08140f", validators=[HEX_COLOR])
    color_primary = models.CharField("Color principal (fondo)", max_length=7, default="#0f2a20", validators=[HEX_COLOR])
    color_accent = models.CharField("Color de detalles (dorado)", max_length=7, default="#e3bd6a", validators=[HEX_COLOR])
    color_magic = models.CharField("Color mágico (violeta)", max_length=7, default="#9b7fe0", validators=[HEX_COLOR])

    # --- Datos legales (se rellenan solos en Aviso legal, Privacidad y Cookies) ---
    legal_owner = models.CharField("Titular (nombre o razón social)", max_length=120, blank=True)
    legal_cif = models.CharField("NIF / CIF", max_length=20, blank=True)
    legal_address = models.CharField("Dirección", max_length=200, blank=True)
    legal_phone = models.CharField("Teléfono", max_length=30, blank=True)
    legal_email = models.EmailField("Correo de contacto para protección de datos", blank=True)
    legal_hosting = models.CharField("Proveedor de hosting", max_length=120, blank=True,
                                     help_text="Ej.: Hetzner Online GmbH (Alemania)")
    legal_retention = models.CharField("Plazo de conservación de los mensajes", max_length=60, default="12 meses")
    legal_updated = models.CharField("Fecha de última actualización de los textos legales", max_length=40, blank=True)

    class Meta:
        verbose_name = "textos y datos de la web"
        verbose_name_plural = "textos y datos de la web"

    def __str__(self):
        return "Textos y datos de la web"

    def save(self, *args, **kwargs):
        self.pk = 1  # solo existe una ficha
        optimize_image(self.home_photo, 1400)
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def instagram_label(self):
        return "@" + self.instagram_handle.lstrip("@") if self.instagram_handle else "Instagram"


# ============================================================================
# CURSOS
# ============================================================================
class Course(models.Model):
    class Level(models.TextChoices):
        ALL = "todos", "Todos los niveles"
        BEGINNER = "principiante", "Principiante"
        MEDIUM = "intermedio", "Intermedio"
        ADVANCED = "avanzado", "Avanzado"

    title = models.CharField("Nombre del curso", max_length=120)
    slug = models.SlugField(max_length=140, unique=True, editable=False)
    summary = models.CharField("Descripción breve", max_length=220,
                               help_text="Se ve en la lista de cursos, antes de entrar en él.")
    description = models.TextField("Descripción completa", blank=True,
                                   help_text="Se ve al entrar en el curso. Línea en blanco = párrafo nuevo. Líneas que empiezan por «- » = lista.")
    level = models.CharField("Nivel", max_length=20, choices=Level.choices, default=Level.ALL)
    duration = models.CharField("Duración", max_length=80, blank=True, help_text="Ej.: 6 sesiones de 90 min")
    modality = models.CharField("Modalidad", max_length=80, blank=True, help_text="Ej.: Online, Presencial en Madrid")
    price_text = models.CharField("Precio", max_length=60, blank=True,
                                  help_text="Ej.: 120 € · Déjalo vacío para mostrar «Consultar precio».")
    image = models.ImageField("Foto del curso", upload_to="cursos/", blank=True, validators=[validate_image_size])
    order = models.PositiveSmallIntegerField("Orden", default=0, help_text="Los más pequeños salen primero.")
    active = models.BooleanField("Visible en la web", default=True)

    class Meta:
        verbose_name = "curso"
        verbose_name_plural = "cursos"
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:100] or "curso"
            slug, n = base, 2
            while Course.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug, n = f"{base}-{n}", n + 1
            self.slug = slug
        optimize_image(self.image, 1400)
        super().save(*args, **kwargs)



class CourseBlock(models.Model):
    """Apartados de un curso (qué aprenderás, temario, requisitos, material...). Tantos como quieras."""

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="blocks")
    title = models.CharField("Título del apartado", max_length=100, help_text="Ej.: Qué aprenderás")
    text = models.TextField("Texto", help_text="Línea en blanco = párrafo nuevo. Líneas que empiezan por «- » = lista. Puedes mezclar texto y listas.")
    order = models.PositiveSmallIntegerField("Orden", default=0)

    class Meta:
        verbose_name = "apartado del curso"
        verbose_name_plural = "apartados del curso"
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


# ============================================================================
# SABER MÁS: carrusel, pasos y preguntas frecuentes
# ============================================================================
class GalleryImage(models.Model):
    image = models.ImageField("Foto", upload_to="carrusel/", validators=[validate_image_size],
                              help_text="Horizontal, mejor 1600×900 px o más grande.")
    caption = models.CharField("Pie de foto (opcional)", max_length=140, blank=True)
    order = models.PositiveSmallIntegerField("Orden", default=0)
    active = models.BooleanField("Visible", default=True)

    class Meta:
        verbose_name = "foto del carrusel"
        verbose_name_plural = "fotos del carrusel"
        ordering = ["order", "id"]

    def __str__(self):
        return self.caption or f"Foto {self.pk}"

    def save(self, *args, **kwargs):
        optimize_image(self.image, 1920)
        super().save(*args, **kwargs)


class Step(models.Model):
    title = models.CharField("Título", max_length=100)
    text = models.TextField("Explicación")
    order = models.PositiveSmallIntegerField("Orden", default=0)
    active = models.BooleanField("Visible", default=True)

    class Meta:
        verbose_name = "paso (cómo funcionan los cursos)"
        verbose_name_plural = "pasos (cómo funcionan los cursos)"
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Faq(models.Model):
    question = models.CharField("Pregunta", max_length=200)
    answer = models.TextField("Respuesta")
    order = models.PositiveSmallIntegerField("Orden", default=0)
    active = models.BooleanField("Visible", default=True)

    class Meta:
        verbose_name = "pregunta frecuente"
        verbose_name_plural = "preguntas frecuentes"
        ordering = ["order", "id"]

    def __str__(self):
        return self.question


# ============================================================================
# MENSAJES RECIBIDOS POR EL FORMULARIO DE CONTACTO
# ============================================================================
class Message(models.Model):
    name = models.CharField("Nombre", max_length=100)
    email = models.EmailField("Email")
    course = models.CharField("Curso por el que pregunta", max_length=140, blank=True)
    message = models.TextField("Mensaje")
    created_at = models.DateTimeField("Recibido", auto_now_add=True)
    is_read = models.BooleanField("Leído", default=False)

    class Meta:
        verbose_name = "mensaje recibido"
        verbose_name_plural = "mensajes recibidos"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} · {self.created_at:%d/%m/%Y %H:%M}"
