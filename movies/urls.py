from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.list, name='list'),
    path('<int:movie_pk>/', views.detail, name="detail"),
    path('<int:movie_pk>/scores/new/', views.new_score, name="new_score"),
    path('<int:movie_pk>/<int:score_pk>/delete/', views.del_score, name="del_score"),
    path('recommendation/', views.recommendation, name='recommendation'),
]