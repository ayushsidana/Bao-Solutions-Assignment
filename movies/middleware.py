from django.http import JsonResponse
from django.conf import settings

class ApiKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.api_key = getattr(settings, 'SECRET_API_KEY')

    def __call__(self, request):
        client_api_key = request.headers.get('Authorization')

        if client_api_key != f"Bearer {self.api_key}":
            return JsonResponse({'error': 'Invalid API key'}, status=401)

        response = self.get_response(request)
        return response
