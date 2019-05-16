import requests
import json
import os
from bs4 import BeautifulSoup

api_key = os.getenv('TMDB_API_KEY')
language = 'ko-KR'

tmdb_id_dict = dict()
score_pk = 0

def get_score_pk():
    global score_pk
    score_pk += 1
    return score_pk

def get_popular_movies():
    '''
    인기순으로 영화들의 정보를 가져와 json파일로 저장,
    creator들도 json형태로 저장.
    '''
    creators = []
    with open(f'movie.json', 'w', encoding='utf-8') as f:
        tot = []
        for i in range(1, 101): # 우선 100 page까지만 해봅시다.
            
            url = f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language={language}&page={i}'
            response = requests.get(url).json()['results']
            for r in response:
                movie_id = r['id']
                movie, tmp_creators = get_movie(movie_id)

                if movie and tmp_creators:
                    tot.append(movie)
                    creators.extend(tmp_creators)
        json.dump(tot, f, ensure_ascii=False, indent="\t")
                
    make_json_creator(creators, 1)

def get_movie(movie_id):
    '''
    해당 id의 영화 정보와 creator들을 반환
    return movie, creators
    '''
    detail_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language={language}'
    detail_response = requests.get(detail_url).json()
    
    actor_url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}'
    actor_response = requests.get(actor_url).json()
    
    director = None
    try:
        for crew in actor_response['crew']:
            if crew['job'] == 'Director':
                director = crew['id']
                break

        movie = {
            'model': 'movies.movie',
            'pk': detail_response['id'],
            'fields': {
                'title': detail_response['title'],
                'original_title': detail_response['original_title'],
                'runtime': detail_response['runtime'],
                'overview': detail_response['overview'],
                'poster_url': f"https://image.tmdb.org/t/p/original/{detail_response['poster_path']}",
                'popularity': detail_response['popularity'],
                'director': director,
                'genres': [genre['id'] for genre in detail_response['genres']],
                'actors': [cast['id'] for cast in actor_response['cast']][:10],
            },
        }
        creators = get_creator(actor_response)
        return movie, creators
    except Exception:
        print(f'{movie_id}실패')
        return None, None
            
def get_genres():
    with open(f'genre.json', 'w', encoding='utf-8') as f:
        url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=ko-KR'
        response = requests.get(url).json()['genres']
        tot = []
        for r in response:
            result = {
                "model": "movies.genre",
                "pk": r['id'],
                "fields": {"name": f"{r['name']}"}
            }
            tot.append(result)
        json.dump(tot, f, ensure_ascii=False, indent="\t")

def get_creator(actor_response):
    '''
        크리에이터에 들어갈 목록을 리턴시킨다.
        배우 10명, 감독 1명을 넣고, 중복은 고려하지 않는다.
        크롤링 페이지 예시 https://api.themoviedb.org/3/movie/212778/credits?api_key={api_key}
        
    '''
    result = []
    for i, cast in enumerate(actor_response['cast']):
        if i==10: break
        result.append(
            {
                'model': 'movies.creator',
                'pk': cast['id'],
                'fields': {
                    'name': cast['name']
                }
            }    
        )
    for crew in actor_response['crew']:
        if crew['job'] == 'Director':
            result.append(
                {
                    'model': 'movies.creator',
                    'pk': crew['id'],
                    'fields': {
                        'name': crew['name']
                    }
                }    
            )
            break
    return result
    
def make_json_creator(creators, mode):
    # creators에서 중복이 있을 수 있으므로 중복을 제거한 후에 파일에 집어넣는다.
    is_overlap = dict()
    unique_result = []
    for creator in creators:
        if not is_overlap.get(creator['pk']):
            is_overlap[creator['pk']] = True
            unique_result.append(creator)
    with open(f'creator{mode}.json', 'w', encoding='utf-8') as f:
        json.dump(unique_result, f, ensure_ascii=False, indent="\t")
        
def get_imdb_movie_id(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}/external_ids?api_key={api_key}'
    return requests.get(url).json().get('imdb_id')


def get_tmdb_movie_id(imdb_id):
    result = tmdb_id_dict.get(imdb_id)
    if result:
        return result

    url = f'https://api.themoviedb.org/3/find/{imdb_id}?api_key={api_key}&language=en-US&external_source=imdb_id'
    response = requests.get(url).json()['movie_results']
    if response:
        tmdb_id_dict[imdb_id] = response[0].get('id')
        return tmdb_id_dict[imdb_id]


def get_user():
    '''
    특정 영화(엔드게임)에 대해 리뷰를 남긴 사람들 200명을 대상으로 각 유저를 생성한다.
    '''
    import sys
    sys.stdin = open('users1.txt')
    users = [input().split() for _ in range(200)]
    # print(users)
    # 유저 집어넣어야함
    return users

def get_scores(users):
    '''
    get_user를 통해 뽑은 200명의 유저에 대해 각 유저별 등록한 평점들을 기록한다.
    '''
    scores = []
    for i, u in enumerate(users):
        tmp_scores = get_scores_from_user(i+1, u[1])
        if tmp_scores:
            scores.extend(tmp_scores)
    with open(f'score.json', 'w', encoding='utf-8') as f:
        json.dump(scores, f, ensure_ascii=False, indent="\t")


def get_scores_from_user(u_id, imdb_u_id):
    '''
    해당 유저가 등록한 스코어들을 가져온다.
    '''
    user_scores = []
    rating_url = f'https://www.imdb.com/user/{imdb_u_id}/ratings'
    
    response = requests.get(rating_url)

    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        ratings = soup.find_all('div', {'class':'lister-item'})
        for rating in ratings:
            try:
                imdb_id = rating.find('h3').find('a')['href'][len('/title/'):-1]
                value = rating.find('div', {'class':'ipl-rating-star--other-user'}).find('span', {'class':'ipl-rating-star__rating'}).text
                movie = get_tmdb_movie_id(imdb_id)
                if movie:
                    user_scores.append(
                        {
                            "model": "movies.score",
                            "pk": get_score_pk(),
                            "fields": {
                                "content": "",
                                "value": value,
                                "movie": movie,
                                "user": u_id
                            }
                        }
                    )
            except Exception:
                continue
    return user_scores

def get_not_in_movies():
    movies = dict()
    scored_movies = []
    not_in_movies = []
    with open('movie.json', encoding='utf-8') as f:
        movies ={movie.get('pk'):True for movie in json.load(f)}

    with open('score_b.json', encoding='utf-8') as f:
        # print(json.load(f)[0])
        scores = json.load(f)
        tmp = [score['fields']['movie'] for score in scores]
        scored_movies = list(set(tmp))

    for scored_movie in scored_movies:
        if not movies.get(scored_movie):
            not_in_movies.append(scored_movie)
    return not_in_movies

def add_movies():
    not_in_movies = get_not_in_movies()
    creators = []
    tot = []
    impossible = []
    for movie_id in not_in_movies:
        print(f'{movie_id} 시도중', end='\r')
        movie, tmp_creators = get_movie(movie_id)
        if movie and tmp_creators:
            tot.append(movie)
            creators.extend(tmp_creators)
        else:
            impossible.append(movie_id)
    with open(f'add_movie.json', 'w', encoding='utf-8') as f:
        json.dump(tot, f, ensure_ascii=False, indent="\t")
                
    with open(f'impossible.json', 'w', encoding='utf-8') as f:
        json.dump(tot, f, ensure_ascii=False, indent="\t")
    
    make_json_creator(creators, 2)

# get_genres()
# get_popular_movies()
# get_scores(get_user())
# add_movies()