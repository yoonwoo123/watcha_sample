from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Score
from .forms import ScoreForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def list(request):
    movies = Movie.objects.order_by('-popularity')
    context = {'movies': movies}
    return render(request, 'movies/list.html', context)
    
def detail(request, movie_pk):
    # score = get_object_or_404(Score, pk=movie_pk)
    score = Score.objects.all()
    score_form = ScoreForm()
    movie_detail = get_object_or_404(Movie, pk=movie_pk)
    context = {'movie_detail': movie_detail, 'score_form': score_form, 'score': score}
    return render(request, 'movies/detail.html', context)

@login_required
def new_score(request, movie_pk):
    if request.method == "POST":
        score_form = ScoreForm(request.POST)
        if score_form.is_valid():
            score = score_form.save(commit=False)
            score.movie_id = movie_pk
            score.user = request.user
            score.save()
        else:
            return redirect('movies:list')
        context = {'score_form': score_form}
        return redirect('movies:detail', movie_pk)
        
def del_score(request, movie_pk, score_pk):
    if request.method == "POST":
        score = get_object_or_404(Score, pk=score_pk)
        score.delete()
        return redirect('movies:detail', movie_pk)
