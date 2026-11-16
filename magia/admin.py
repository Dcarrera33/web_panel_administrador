"""Panel de administración (http://tudominio/gestion/).

Desde aquí el dueño cambia TODO el contenido de la web sin tocar código: los textos y la foto de
inicio, los cursos (con sus apartados), el carrusel de «Saber más», los pasos y las preguntas
frecuentes, y lee los mensajes que llegan por el formulario de contacto.
"""
from django import forms
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html

from .models import Course, CourseBlock, Faq, GalleryImage, Message, SiteContent, Step

admin.site.site_header = "Magia en el bosque · Panel de gestión"
admin.site.site_title = "Panel de gestión"
admin.site.index_title = "Gestión de la web"


def _thumb(image):
    if not image:
        return "—"
    return format_html('<img class="thumb" src="{}" alt="">', image.url)


# ==========================================================================
# TEXTOS Y DATOS DE LA WEB (una sola ficha)
# ==========================================================================
class ColorInput(forms.TextInput):
    input_type = "color"


class SiteContentForm(forms.ModelForm):
    class Meta:
        model = SiteContent
        fields = "__all__"
        widgets = {f: ColorInput(attrs={"class": "color-pick"})
                   for f in ("color_dark", "color_primary", "color_accent", "color_magic")}


@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    form = SiteContentForm
    fieldsets = (
        ("Inicio: foto a la izquierda, texto a la derecha", {
            "fields": ("home_photo", "home_kicker", "home_title", "home_text", "home_signature", "home_button_text")}),
        ("Cabecera y pie de página", {"fields": ("site_name", "tagline", "footer_text")}),
        ("Saber más", {"fields": ("about_title", "about_intro")}),
        ("Contacto e Instagram", {"fields": ("contact_intro", "contact_email", "instagram_handle", "instagram_url")}),
        ("Colores (opcional)", {"classes": ("collapse",),
                                "fields": ("color_dark", "color_primary", "color_accent", "color_magic")}),
        ("Datos legales (aviso legal, privacidad y cookies)", {"classes": ("collapse",), "fields": (
            "legal_owner", "legal_cif", "legal_address", "legal_phone", "legal_email", "legal_hosting",
            "legal_retention", "legal_updated")}),
    )

    def has_add_permission(self, request):
        return False  # solo existe una ficha

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        # No hay lista: se entra directamente a editar la única ficha
        SiteContent.load()
        return HttpResponseRedirect(reverse("admin:magia_sitecontent_change", args=[1]))

    def response_change(self, request, obj):
        if "_save" in request.POST:
            self.message_user(request, "Cambios guardados. Ya se ven en la web.", messages.SUCCESS)
            return HttpResponseRedirect(reverse("admin:index"))
        return super().response_change(request, obj)


# ==========================================================================
# CURSOS
# ==========================================================================
class CourseBlockInline(admin.StackedInline):
    model = CourseBlock
    extra = 1
    fields = ("title", "text", "order")
    classes = ("block-inline",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("photo", "title", "level", "price_text", "active", "order")
    list_display_links = ("photo", "title")
    list_editable = ("price_text", "active", "order")
    list_filter = ("active", "level")
    search_fields = ("title", "summary")
    inlines = [CourseBlockInline]
    actions = ["hide", "show"]
    fieldsets = (
        ("Lo que se ve en la lista de cursos", {"fields": ("title", "summary", "image")}),
        ("Al entrar en el curso", {"fields": ("description", "level", "duration", "modality", "price_text"),
                                   "description": "Debajo puedes añadir apartados: qué aprenderás, temario, requisitos..."}),
        ("Visibilidad", {"fields": ("active", "order")}),
    )

    @admin.display(description="Foto")
    def photo(self, obj):
        return _thumb(obj.image)

    @admin.action(description="Ocultar de la web")
    def hide(self, request, queryset):
        n = queryset.update(active=False)
        self.message_user(request, f"{n} curso(s) ocultados de la web.", messages.SUCCESS)

    @admin.action(description="Volver a mostrar en la web")
    def show(self, request, queryset):
        n = queryset.update(active=True)
        self.message_user(request, f"{n} curso(s) visibles de nuevo.", messages.SUCCESS)


# ==========================================================================
# SABER MÁS
# ==========================================================================
@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("photo", "caption", "active", "order")
    list_display_links = ("photo", "caption")
    list_editable = ("active", "order")

    @admin.display(description="Foto")
    def photo(self, obj):
        return _thumb(obj.image)


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ("title", "short_text", "active", "order")
    list_editable = ("active", "order")

    @admin.display(description="Explicación")
    def short_text(self, obj):
        return (obj.text[:70] + "…") if len(obj.text) > 70 else obj.text


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ("question", "active", "order")
    list_editable = ("active", "order")


# ==========================================================================
# MENSAJES DEL FORMULARIO DE CONTACTO
# ==========================================================================
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("state", "name", "email", "course", "short_message", "created_at")
    list_display_links = ("name",)
    list_filter = ("is_read",)
    search_fields = ("name", "email", "message", "course")
    actions = ["mark_read", "mark_unread"]
    fields = ("name", "email", "course", "message", "created_at", "is_read")
    readonly_fields = ("name", "email", "course", "message", "created_at")

    def has_add_permission(self, request):
        return False  # los mensajes solo llegan por la web

    @admin.display(description="")
    def state(self, obj):
        if obj.is_read:
            return ""
        return format_html('<span class="new-badge">NUEVO</span>')

    @admin.display(description="Mensaje")
    def short_message(self, obj):
        return (obj.message[:60] + "…") if len(obj.message) > 60 else obj.message

    def change_view(self, request, object_id, form_url="", extra_context=None):
        # Al abrir un mensaje por primera vez se marca como leído
        if request.method == "GET":
            Message.objects.filter(pk=object_id, is_read=False).update(is_read=True)
        return super().change_view(request, object_id, form_url, extra_context)

    @admin.action(description="Marcar como leídos")
    def mark_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description="Marcar como no leídos")
    def mark_unread(self, request, queryset):
        queryset.update(is_read=False)
