"""Convierte el texto escrito en el panel en HTML ordenado.

Reglas (las mismas para todos los textos largos de la web):
- Una LÍNEA EN BLANCO separa párrafos.
- Un salto de línea normal dentro de un párrafo se respeta (sale en otra línea).
- Las líneas que empiezan por «- » (o «* », «• ») forman una LISTA con estrellitas.
- Funciona igual con saltos de línea de Windows (\\r\\n), Mac o Linux.
"""
import re

from django.utils.html import escape
from django.utils.safestring import mark_safe

BULLET = re.compile(r"^\s*(?:[-*•–])\s+(.*\S)\s*$")


def parse_blocks(text):
    """-> [("p", [líneas]), ("ul", [elementos])] respetando el orden del texto."""
    blocks, para, items = [], [], []

    def flush_para():
        if para:
            blocks.append(("p", para[:]))
            para.clear()

    def flush_items():
        if items:
            blocks.append(("ul", items[:]))
            items.clear()

    for raw in (text or "").replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        line = raw.strip()
        m = BULLET.match(raw)
        if not line:                      # línea en blanco: termina el bloque actual
            flush_para(); flush_items()
        elif m:                           # línea de lista
            flush_para(); items.append(m.group(1).strip())
        else:                             # línea de texto normal
            flush_items(); para.append(line)
    flush_para(); flush_items()
    return blocks


def render_text(text):
    out = []
    for kind, lines in parse_blocks(text):
        if kind == "p":
            out.append("<p>" + "<br>".join(escape(x) for x in lines) + "</p>")
        else:
            out.append('<ul class="starlist">' + "".join(f"<li>{escape(x)}</li>" for x in lines) + "</ul>")
    return mark_safe("".join(out))
