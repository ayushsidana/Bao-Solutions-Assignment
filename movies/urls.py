from django.urls import path
from .views import MovieListView, ExternalMovies

urlpatterns = [
    path('movies/', MovieListView.as_view(), name='movie-list'),
    path('external-movies/', ExternalMovies.as_view(), name='external-movies'),
]
