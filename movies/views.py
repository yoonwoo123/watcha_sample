from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Score
from .forms import ScoreForm
from django.contrib.auth.decorators import login_required
from .recommendations import get_recommendations, top_matches
# Create your views here.
def list(request):
    movies = Movie.objects.order_by('-popularity')
    context = {'movies': movies}
    return render(request, 'movies/list.html', context)
    
def detail(request, movie_pk):
    # score = get_object_or_404(Score, pk=movie_pk)
    score = Score.objects.all()
    score_form = ScoreForm()
    movie = get_object_or_404(Movie, pk=movie_pk)
    context = {'movie': movie, 'score_form': score_form, 'score': score}
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

    
@login_required
def recommendation(request):
    scores = Score.objects.all()
    r_model = dict()
    for score in scores:
        if r_model.get(score.user.pk):
            r_model[score.user.pk][score.movie.pk] = score.value
        else:
            r_model[score.user.pk] = {score.movie.pk : score.value}
            
    movie_ids = get_recommendations(r_model, request.user.pk)
    # t_match = top_matches(r_model, request.user.pk)
    
    movies = Movie.objects.filter(pk__in=movie_ids)
    # movies = Movie.objects.all()
    print(movies)
    context = {
        # 'r_model':r_model,
        'movies':movies,
        # 'result2':t_match,
    }
    # print('결과')
    # print(t_match)
    return render(request, 'movies/list.html', context)
    