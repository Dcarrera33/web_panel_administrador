"""Envío de emails con Gmail (a través de los ajustes de Django).

Sin GMAIL_USER / GMAIL_APP_PASSWORD en .env, los emails se imprimen en el terminal.
"""
import logging
import threading

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

log = logging.getLogger("emails")


def _one_line(value):
    return " ".join(str(value).split())


def _deliver(subject, text, html, to, reply_to, from_name):
    try:
        sender = f"{_one_line(from_name)} <{settings.DEFAULT_FROM_EMAIL}>"
        msg = EmailMultiAlternatives(
            _one_line(subject), text, sender, [_one_line(to)],
            reply_to=[_one_line(reply_to)] if reply_to else None,
        )
        msg.attach_alternative(html, "text/html")
        msg.send()
    except Exception:
        # Si falla el email, el mensaje ya está guardado en el panel: solo lo registramos.
        log.exception("No se pudo enviar el email a %s", to)


def send_email(to, subject, text, html, reply_to=None, from_name="Contacto"):
    """Envía en segundo plano para que la web no se quede esperando a Gmail."""
    args = (subject, text, html, to, reply_to, from_name)
    if settings.EMAIL_ASYNC:
        threading.Thread(target=_deliver, args=args, daemon=True).start()
    else:
        _deliver(*args)


def notify_message(msg, site):
    """Aviso al dueño de la web: ha llegado un mensaje por el formulario de contacto."""
    to = settings.NOTIFY_EMAIL
    if not to:
        print("[AVISO] Falta NOTIFY_EMAIL/GMAIL_USER en .env: el mensaje solo queda guardado en el panel.", flush=True)
        return
    about = f" · {msg.course}" if msg.course else ""
    subject = f"Nuevo mensaje de {_one_line(msg.name)}{about}"
    text = (f"NUEVO MENSAJE DE CONTACTO\n\nNombre: {msg.name}\nEmail: {msg.email}\n"
            f"Curso: {msg.course or '-'}\n\n{msg.message}\n")
    html = render_to_string("magia/email/contacto.html", {"m": msg, "site": site})
    send_email(to, subject, text, html, reply_to=msg.email, from_name=site.site_name)
