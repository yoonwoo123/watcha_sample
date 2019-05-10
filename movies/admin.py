from django.contrib import admin
from .models import Movie, Genre
# Register your models here.
class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'movie_id', 'title']
    
class GenreAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    
admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre, GenreAdmin)