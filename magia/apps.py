from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class MagiaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "magia"
    verbose_name = "Magia en el bosque"


class MagiaAdminConfig(AdminConfig):
    """Usa nuestro panel (con portada propia) en lugar del de Django por defecto."""

    default_site = "magia.sites.MagiaAdminSite"
