import uuid
from django.db import models
from django.utils import timezone


class Species(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    classification = models.CharField(max_length=255)
    eye_colors = models.CharField(max_length=255)
    hair_colors = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.name

class Actor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    age = models.CharField(max_length=10)
    eye_color = models.CharField(max_length=20)
    hair_color = models.CharField(max_length=20)
    species = models.ForeignKey(Species, on_delete=models.CASCADE)
    url = models.URLField()

    def __str__(self):
        return self.name

class Movie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255)
    original_title_romanised = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    director = models.CharField(max_length=255)
    producer = models.CharField(max_length=255)
    release_date = models.CharField(max_length=4)  # Assuming it's a year
    running_time = models.PositiveIntegerField()   # Assuming it's in minutes
    rt_score = models.PositiveIntegerField()
    actors = models.ManyToManyField(Actor, related_name='movies')

    CACHE_KEY = 'external_movies_data'

    @property
    def is_fresh(self):
        return timezone.now() - self.created_at < timezone.timedelta(minutes=1)

    def __str__(self):
        return self.title