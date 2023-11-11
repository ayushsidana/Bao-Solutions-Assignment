import requests
from datetime import datetime
from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .utils import get_cached_data, set_cached_data
from .models import Movie
from .client import ExternalAPIClient
from .constants import API_URL
from .serializers import MovieSerializer, MovieBaseSerializer

class ExternalMovies(APIView):
    """
    API endpoint for external movies data.
    """
    
    def is_data_expired(self):
        """
        Check if cached data is expired.
        """
        return not get_cached_data(settings.EXTERNAL_MOVIES_CACHE_KEY)

    def call_external_api(self, url):
        """
        Make a call to the external API and return the response.
        """
        return ExternalAPIClient.call_api(url)

    def extract_species_details(self, species_url):
        """
        Extract species details from the provided species URL.
        """
        species_details = self.call_external_api(species_url)
        return {
            "name": species_details.get("name"),
            "classification": species_details.get("classification"),
        } if isinstance(species_details, dict) else None

    def fetch_data_from_api(self):
        """
        Fetch data from the external API and update the cache.
        """
        try:
            movies_data = self.call_external_api(API_URL)
            if movies_data:
                self.extract_actor_data(movies_data)
                set_cached_data(settings.EXTERNAL_MOVIES_CACHE_KEY, {'timestamp': datetime.now(), 'data': movies_data})
                return Response(movies_data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Failed to fetch data from the external API"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except requests.HTTPError as e:
            # Handle HTTP errors (4xx and 5xx)
            return Response({"error": str(e)}, status=e.response.status_code)

    def extract_actor_data(self, movies_data):
        """
        Extract actor data from the movies data.
        """
        for movie in movies_data:
            people_extracted_data = []
            people_urls = movie.pop("people", [])

            for people_url in people_urls:
                people_details = self.call_external_api(people_url)
                if isinstance(people_details, dict):
                    actor_some_details = {
                        "id": people_details["id"],
                        "name": people_details["name"],
                        "url": people_details["url"],
                        "species": self.extract_species_details(people_details["species"])
                    }
                    people_extracted_data.append(actor_some_details)

            movie["actors"] = people_extracted_data

    def get(self, request, *args, **kwargs):
        """
        Handle GET request for which django acts as a service provider to get list of movies.
        """
        if self.is_data_expired():
            response = self.fetch_data_from_api()
            return response

        movies_data = get_cached_data(settings.EXTERNAL_MOVIES_CACHE_KEY)['data']
        movie_serializer = MovieBaseSerializer(movies_data, many=True)
        return Response(movie_serializer.data, status=status.HTTP_200_OK)


class MovieListView(ListAPIView):
    """
    List view for fresh movies.
    """
    
    serializer_class = MovieSerializer

    def get_queryset(self):
        """
        Get fresh movies from the cache or fetch from the database if not available.
        """
        fresh_movies = get_cached_data(settings.EXTERNAL_MOVIES_CACHE_KEY)

        if fresh_movies is None:
            # If not in cache or cache is expired, fetch fresh movies
            one_minute_ago = timezone.now() - timezone.timedelta(minutes=1)
            fresh_movies = Movie.objects.filter(created_at__gte=one_minute_ago)

            # Cache the result
            set_cached_data(settings.EXTERNAL_MOVIES_CACHE_KEY, fresh_movies)

        return fresh_movies
