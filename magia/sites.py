"""Panel de gestión: portada propia con mensajes nuevos, accesos directos y resumen."""
from django.contrib import admin
from django.utils import timezone

from .models import Course, GalleryImage, Message

MODEL_ORDER = ["sitecontent", "course", "galleryimage", "step", "faq", "message"]


class MagiaAdminSite(admin.AdminSite):
    index_template = "admin/dashboard.html"

    def get_app_list(self, request, app_label=None):
        """Ordena los apartados del panel: textos de la web, cursos, carrusel..., mensajes."""
        apps = super().get_app_list(request, app_label)
        apps.sort(key=lambda app: app["app_label"] != "magia")  # lo de la web, antes que usuarios y grupos
        for app in apps:
            if app["app_label"] == "magia":
                app["models"].sort(key=lambda m: MODEL_ORDER.index(m["object_name"].lower())
                                   if m["object_name"].lower() in MODEL_ORDER else 99)
        return apps

    def index(self, request, extra_context=None):
        unread = Message.objects.filter(is_read=False)
        context = dict(
            today=timezone.localdate(),
            unread_count=unread.count(),
            latest_messages=Message.objects.all()[:6],
            course_count=Course.objects.filter(active=True).count(),
            hidden_courses=Course.objects.filter(active=False).count(),
            photo_count=GalleryImage.objects.filter(active=True).count(),
        )
        context.update(extra_context or {})
        return super().index(request, context)
