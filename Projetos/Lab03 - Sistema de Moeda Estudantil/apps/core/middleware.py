from django.utils.deprecation import MiddlewareMixin

class SimpleSecurityHeaders(MiddlewareMixin):
    def process_response(self, request, response):
        response["X-Frame-Options"] = "DENY"
        response["X-Content-Type-Options"] = "nosniff"
        return response
