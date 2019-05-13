from django.db import models
from django.conf import settings

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
    popularity = models.FloatField()
    actors = models.ManyToManyField(Creator, related_name='movies')
    director = models.ForeignKey(Creator, on_delete=models.CASCADE)

class Score(models.Model):
    content = models.CharField(max_length=140)
    value = models.FloatField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    class Meta: # 메타 정보 : 일관성있는 정보 -> 모든 클래스에는 메타정보를 담을 수 있다.
        ordering = ['-value'] # 원래 pk값 순서로 갖고오나 이렇게 설정하면 value의 내림차순('-')으로 갖고옴
