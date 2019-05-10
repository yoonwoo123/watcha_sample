from django.db import models

# Create your models here.
class Genre(models.Model):
    name = models.TextField()
    
# class Actor(models.Model):
    # actor_id = models.IntegerField()
    
class Movie(models.Model):
    movie_id = models.IntegerField()
    title = models.TextField()
    original_title = models.TextField()
    runtime = models.IntegerField()
    genres = models.ManyToManyField(Genre, related_name='movies')
    overview = models.TextField()
    poster_url = models.TextField()
    popularity = models.IntegerField()
    # actors = models.ManyToManyField(Actor, related_name='movies')
    director = models.TextField()
