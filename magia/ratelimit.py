"""Limitador sencillo de intentos por IP (anti-spam y anti-fuerza-bruta)."""
from functools import wraps

from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render


def client_ip(request):
    if settings.TRUST_PROXY:
        # El último valor lo añade nuestro proxy de confianza; los anteriores los puede falsear el cliente
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
        if forwarded:
            return forwarded.split(",")[-1].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


def rate_limit(name, limits, methods=("POST",)):
    """limits = [(máx_intentos, segundos), ...]  Ej: [(6, 60), (40, 86400)]"""

    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if settings.RATE_LIMIT_ENABLED and request.method in methods:
                ip = client_ip(request)
                for max_hits, seconds in limits:
                    key = f"rl:{name}:{seconds}:{ip}"
                    cache.add(key, 0, seconds)
                    try:
                        hits = cache.incr(key)
                    except ValueError:
                        cache.set(key, 1, seconds)
                        hits = 1
                    if hits > max_hits:
                        return render(request, "magia/error.html",
                                      {"code": 429, "message": "Demasiados intentos seguidos. Espera un momento e inténtalo de nuevo."},
                                      status=429)
            return view(request, *args, **kwargs)

        return wrapper

    return decorator
