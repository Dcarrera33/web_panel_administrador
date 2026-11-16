"""Variables disponibles en TODAS las plantillas."""
from django.utils import timezone

from .models import SiteContent


def site(request):
    return {"site": SiteContent.load(), "year": timezone.localdate().year}
