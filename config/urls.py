from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# El panel de administración está en /gestion/ (más difícil de adivinar que /admin/)
urlpatterns = [
    path("gestion/", admin.site.urls),
    path("", include("magia.urls")),
]

# En desarrollo, Django sirve las fotos subidas. En producción las sirve el hosting (ver README).
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "magia.views.error_404"
handler403 = "magia.views.error_403"
handler500 = "magia.views.error_500"
