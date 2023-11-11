from rest_framework.authentication import BaseAuthentication

class ApiKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('Authorization')

        # Replace 'your_secret_key' with a secure value of your choice
        if api_key != 'Bearer ghiblikey':
            return None

        return ('API_KEY', None)