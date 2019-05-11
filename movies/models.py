from django.db import models

# Create your models here.
class Creator(models.Model): # 감독과 배우 모두 들어있는 클래스
    name = models.TextField()
    
class Genre(models.Model):
    name = models.TextField()
    
class Movie(models.Model):
    title = models.TextField()
    original_title = models.TextField()
    runtime = models.IntegerField()
    genres = models.ManyToManyField(Genre, related_name='movies')
    overview = models.TextField()
    poster_url = models.TextField()
    popularity = models.IntegerField()
    actors = models.ManyToManyField(Creator, related_name='movies')
    director = models.ForeignKey(Creator, on_delete=models.CASCADE)
