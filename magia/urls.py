from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cursos/", views.cursos, name="cursos"),
    path("cursos/<slug:slug>/", views.curso_detalle, name="curso"),
    path("saber-mas/", views.saber_mas, name="saber_mas"),
    path("contacto/", views.contacto, name="contacto"),
    path("contacto/enviado/", views.contacto_ok, name="contacto_ok"),
    path("legal/<slug:page>/", views.legal, name="legal"),
    path("theme.css", views.theme_css, name="theme_css"),
]
