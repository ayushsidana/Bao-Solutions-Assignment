import requests

class ExternalAPIClient:
    @staticmethod
    def call_api(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            # Log or handle the exception as needed
            return None
