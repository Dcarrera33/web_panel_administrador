"""Etiquetas y filtros para las plantillas."""
from django import template
from django.utils.safestring import mark_safe

from magia.text import render_text

register = template.Library()

# Iconos SVG (estilo Feather, licencia MIT)
_ICONS = {
    "mail": '<path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/>',
    "instagram": '<rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "pin": '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "star": '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
    "arrow-left": '<line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/>',
    "arrow-right": '<line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>',
}


@register.simple_tag
def icon(name, size=22):
    return mark_safe(
        f'<svg class="icon" viewBox="0 0 24 24" width="{int(size)}" height="{int(size)}" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        + _ICONS.get(name, "") + "</svg>"
    )


LEVEL_ICON_COUNT = {"todos": 0, "principiante": 1, "intermedio": 2, "avanzado": 3}


@register.filter
def level_stars(level):
    """Número de estrellitas según el nivel (para dibujarlas en la tarjeta)."""
    return range(LEVEL_ICON_COUNT.get(level, 0))


@register.filter
def richtext(value):
    """Texto del panel -> párrafos, saltos de línea y listas (ver magia/text.py)."""
    return render_text(value)
