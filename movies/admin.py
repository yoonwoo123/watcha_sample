from django.contrib import admin
from .models import Movie, Genre, Creator, Score
# Register your models here.
class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    
class GenreAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class CreatorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
class ScoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'movie', 'user', 'value']

admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Creator, CreatorAdmin)
admin.site.register(Score, ScoreAdmin)