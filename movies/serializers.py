from rest_framework import serializers
from .models import Movie, Actor, Species

class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = ['id', 'name', 'classification', 'eye_colors', 'hair_colors']

class ActorSerializer(serializers.ModelSerializer):
    species = SpeciesSerializer(read_only=True)

    class Meta:
        model = Actor
        fields = ['id', 'name', 'species', 'url']

class MovieSerializer(serializers.ModelSerializer):
    actors = ActorSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'actors', 'created_at']

class SpeciesBaseSerializer(serializers.Serializer):
    name = serializers.CharField()
    classification = serializers.CharField()

class ActorBaseSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    url = serializers.URLField()
    species = SpeciesBaseSerializer()

class MovieBaseSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    director = serializers.CharField()
    producer = serializers.CharField()
    release_date = serializers.DateField()
    rt_score = serializers.CharField()
    actors = ActorBaseSerializer(many=True)
