from django.contrib import admin
from .models import Movie, Actor, Species

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description']

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'species', 'url']

@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'classification', 'eye_colors', 'hair_colors', 'url']
