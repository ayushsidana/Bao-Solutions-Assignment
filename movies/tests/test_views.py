from unittest.mock import patch, Mock
from django.conf import settings
from rest_framework import status
from django.core.cache import cache
from django.test import TestCase
from rest_framework.test import APIClient
import requests

class ExternalMoviesAPITestCase(TestCase):
    API_URL = '/api/external-movies/'

    def setUp(self):
        self.CACHE_KEY = settings.EXTERNAL_MOVIES_CACHE_KEY
        self.client = APIClient()

    def get_authorization_header(self, api_key='ghiblikey'):
        return {'Authorization': f'Bearer {api_key}'}

    def test_fetch_data_from_api_success(self):
        headers = self.get_authorization_header()
        with patch('movies.views.ExternalAPIClient.call_api') as mock_call_api:
            responses = [
                [
                    {
                        "id": "2baf70d1-42bb-4437-b551-e5fed5a87abe",
                        "title": "Castle in the Sky",
                        "original_title": "天空の城ラピュタ",
                        "original_title_romanised": "Tenkū no shiro Rapyuta",
                        "image": "https://image.tmdb.org/t/p/w600_and_h900_bestv2/npOnzAbLh6VOIu3naU5QaEcTepo.jpg",
                        "movie_banner": "https://image.tmdb.org/t/p/w533_and_h300_bestv2/3cyjYtLWCBE1uvWINHFsFnE8LUK.jpg",
                        "description": "The orphan Sheeta inherited a mysterious crystal that links her to the mythical sky-kingdom of Laputa. With the help of resourceful Pazu and a rollicking band of sky pirates, she makes her way to the ruins of the once-great civilization. Sheeta and Pazu must outwit the evil Muska, who plans to use Laputa's science to make himself ruler of the world.",
                        "director": "Hayao Miyazaki",
                        "producer": "Isao Takahata",
                        "release_date": "1986",
                        "running_time": "124",
                        "rt_score": "95",
                        "people": [
                            "https://ghibliapi.vercel.app/people/598f7048-74ff-41e0-92ef-87dc1ad980a9",
                        ],
                        "species": [
                            "https://ghibliapi.vercel.app/species/af3910a6-429f-4c74-9ad5-dfe1c4aa04f2"
                        ],
                        "locations": [
                            "https://ghibliapi.vercel.app/locations/"
                        ],
                        "vehicles": [
                            "https://ghibliapi.vercel.app/vehicles/4e09b023-f650-4747-9ab9-eacf14540cfb"
                        ],
                        "url": "https://ghibliapi.vercel.app/films/2baf70d1-42bb-4437-b551-e5fed5a87abe"
                    }
                ],
                {
                    "id": "598f7048-74ff-41e0-92ef-87dc1ad980a9",
                    "name": "Lusheeta Toel Ul Laputa",
                    "species": "https://ghibliapi.vercel.app/species/af3910a6-429f-4c74-9ad5-dfe1c4aa04f2",
                    "url": "https://ghibliapi.vercel.app/people/598f7048-74ff-41e0-92ef-87dc1ad980a9"
                },
                {
                    "id": "af3910a6-429f-4c74-9ad5-dfe1c4aa04f2",
                    "name": "Human",
                    "classification": "Mammal",
                },
            ]

            # Set up side_effect to return responses in order
            mock_call_api.side_effect = responses

            response = self.client.get(self.API_URL, headers=headers)
        
        expected_data = [
            {
                'id': '2baf70d1-42bb-4437-b551-e5fed5a87abe',
                'title': 'Castle in the Sky',
                'original_title': '天空の城ラピュタ',
                'original_title_romanised': 'Tenkū no shiro Rapyuta',
                'image': 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/npOnzAbLh6VOIu3naU5QaEcTepo.jpg',
                'movie_banner': 'https://image.tmdb.org/t/p/w533_and_h300_bestv2/3cyjYtLWCBE1uvWINHFsFnE8LUK.jpg',
                'description': "The orphan Sheeta inherited a mysterious crystal that links her to the mythical sky-kingdom of Laputa. With the help of resourceful Pazu and a rollicking band of sky pirates, she makes her way to the ruins of the once-great civilization. Sheeta and Pazu must outwit the evil Muska, who plans to use Laputa's science to make himself ruler of the world.",
                'director': 'Hayao Miyazaki',
                'producer': 'Isao Takahata',
                'release_date': '1986',
                'running_time': '124',
                'rt_score': '95',
                'species': ['https://ghibliapi.vercel.app/species/af3910a6-429f-4c74-9ad5-dfe1c4aa04f2'],
                'locations': ['https://ghibliapi.vercel.app/locations/'],
                'vehicles': ['https://ghibliapi.vercel.app/vehicles/4e09b023-f650-4747-9ab9-eacf14540cfb'],
                'url': 'https://ghibliapi.vercel.app/films/2baf70d1-42bb-4437-b551-e5fed5a87abe',
                'actors': [
                    {
                        'id': '598f7048-74ff-41e0-92ef-87dc1ad980a9',
                        'name': 'Lusheeta Toel Ul Laputa',
                        'url': 'https://ghibliapi.vercel.app/people/598f7048-74ff-41e0-92ef-87dc1ad980a9',
                        'species': {'name': 'Human', 'classification': 'Mammal'}
                    }
                ]
            }
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
        self.assertTrue(cache.get(self.CACHE_KEY))

        # Add a test case to check if cached data is used for subsequent requests
        response = self.client.get(self.API_URL, headers=headers)
        self.assertTrue(cache.get(self.CACHE_KEY))
    
    def test_fetch_data_from_api_failure(self):
        with patch('movies.views.ExternalAPIClient.call_api') as mock_call_api:
            # Simulate failure in external API call
            mock_call_api.return_value = None

            headers = self.get_authorization_header()
            response = self.client.get(self.API_URL, headers=headers)

            self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
            self.assertFalse(cache.get(self.CACHE_KEY))
    
    def test_fetch_data_from_api_http_error(self):
        with patch('movies.views.ExternalAPIClient.call_api') as mock_call_api:
            # Simulate HTTP error in external API call
            mock_call_api.side_effect = requests.HTTPError(response=Mock(status_code=status.HTTP_404_NOT_FOUND))

            headers = self.get_authorization_header()
            response = self.client.get(self.API_URL, headers=headers)

            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            self.assertFalse(cache.get(self.CACHE_KEY))
    
    def test_fetch_data_from_api_invalid_api_key(self):
        headers = self.get_authorization_header(api_key='invalid_api_key')
        headers = {'Authorization': 'Bearer invalid_api_key'}
        response = self.client.get(self.API_URL, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()["error"], "Invalid API key")
        self.assertFalse(cache.get(self.CACHE_KEY))
