"""Cabeceras de seguridad extra. El panel (/gestion/) tiene sus propios estilos y scripts,
por eso la política estricta solo se aplica a la web pública."""


class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith("/gestion"):
            response["Cache-Control"] = "no-store"
        else:
            response["Content-Security-Policy"] = (
                "default-src 'self'; img-src 'self' data:; frame-ancestors 'none'; "
                "base-uri 'self'; form-action 'self'"
            )
        return response
