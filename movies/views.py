from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, Comment
from .forms import ReviewForm, CommentForm, MovieCreationForm
from django.contrib.auth.decorators import login_required

# 페이지네이션
from django.core.paginator import Paginator

# 비동기
from django.http import JsonResponse
from django.http import HttpResponse

# 검색
from django.core import serializers
import json
import time

# 추천
import random
from django.db.models import Count, Avg, Min, Max, Sum
# Create your views here.

def home(request):
    return render(request, 'movies/home.html')

def search(request):
    # 검색어 
    word = request.GET.get('inputText')
    # Q 객체를 사용해서 검색한다. 
    # title,context 칼럼에 대소문자를 구분하지 않고 단어가 포함되어있는지 (icontains) 검사 
    # 중복을 제거한다. 
    if word != '':
        results = Movie.objects.filter(title__icontains=word)
        if len(results) > 10:
            results = results[:10]
        
        if len(results) < 10:
            time.sleep(0.3)
        
        print(word, len(results))
        json_results = serializers.serialize('json', results)
    else:
        json_results = {}
    return HttpResponse(json_results, content_type="text/json-comment-filtered") 

def index(request):
    # 모든 영화 보여주기
    # movies = Movie.objects.all()
    # paginator = Paginator(movies, 8)
    
    # page_number = request.GET.get('page')
    
    # page_obj = paginator.get_page(page_number)
    # context = {
    #     'movies': movies,
    #     'page_obj': page_obj,
    # }
    # return render(request, 'movies/index.html', context)
    
    # 랜덤 영화 보여주기
    # max_id = Movie.objects.all().aggregate(max_id=Max("id"))['max_id']
    # movies = []
    # while len(movies) < 1:
    #     pk = random.randint(1, max_id)
    #     movie = Movie.objects.filter(pk=pk).first()
    #     if movie:
    #         movies.append(movie)
    # context = {
    #     'movies': movies[:9],
    #     'new_one': movies[-1],
    # }

    # 속도 개선
    movies = Movie.objects.all()
    random_movies = []

    while len(random_movies) < 13:
        idx = random.randint(0, len(movies)-1)
        random_movies.append(movies[idx])
    
    context = {
        'movies': random_movies[:12],
        'new_one': random_movies[-1]
    }

    return render(request, 'movies/index.html', context)

# 관리자_영화정보 등록/수정/삭제
def movie_create(request):
    if not request.user.is_superuser:
        return redirect('movies:index')
    if request.method == 'POST':
        form = MovieCreationForm(request.POST)
        if form.is_valid:
            movie = form.save()
            return redirect('movies:detail', movie.pk)
    else:
        form = MovieCreationForm()
    context = {
        'form':form
    }
    return render(request, 'movies/form.html', context)

def movie_update(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if not request.user.is_superuser:
        return redirect('movies:index')
    if request.method == 'POST':
        form = MovieCreationForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movies:detail', movie_pk)
    else:
        form = MovieCreationForm(instance=movie)
    context = {
        'form':form,
        'movie':movie # movie 정보 보내주기(delete 기능 넣기 위해)
    }
    return render(request, 'movies/form.html', context)

def movie_delete(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if not request.user.is_superuser:
        return redirect('movies:index')
        # 메세지 넣기
    movie.delete()
    return redirect('movies:index')
    

def detail(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    genres = movie.genres.values('name')
    context = {
        'movie': movie,
        'genres': genres,
    }
    return render(request, 'movies/detail.html', context)

def like(request, movie_pk):
    user = request.user
    movie = Movie.objects.get(pk=movie_pk)

    if movie.like_users.filter(pk=user.pk).exists():
        movie.like_users.remove(user)
        status = False
    else:
        movie.like_users.add(user)
        status = True
    data = {
        'status': status,
        'count': movie.like_users.count()
    }

    return JsonResponse(data)

@login_required
def review_create(request, movie_pk):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = Movie.objects.get(pk=movie_pk)
            review.save()
            return redirect('movies:review_detail', movie_pk, review.pk)
    else:
        form = ReviewForm()
    context = {
        'form': form,
    }
    return render(request, 'movies/form.html', context)

def review_detail(request, movie_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    # if request.method == 'POST':
    #     form = CommentForm(request.POST)
    #     if form.is_valid():
    #         comment = form.save(commit=False)
    #         comment.review = Review.objects.get(pk=review_pk)
    #         comment.user = request.user
    #         comment.save()
    #         return redirect('movies:review_detail', movie_pk, review_pk)
    # else:
    #     form = CommentForm()
    context = {
        'review': review,
        # 'form': form,
        'movie_pk': movie_pk,
    }
    return render(request, 'movies/review_detail.html', context)

@login_required
def review_delete(request, movie_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.user or request.user.is_superuser:
        review.delete()
    return redirect('movies:detail', movie_pk)

@login_required
def review_update(request, movie_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.method == 'POST':
        if request.user == review.user:
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                return redirect('movies:review_detail', movie_pk, review_pk)
    
    else:
        form = ReviewForm(instance=review)
    context = {
        'form': form,
        'movie_pk': movie_pk,
        'review_pk': review_pk,
    }
    return render(request, 'movies/form.html', context)

def comment_delete(request, movie_pk, review_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user or request.user.is_superuser:
        comment.delete()
    return redirect('movies:review_detail', movie_pk, review_pk)

def comment_create(request, movie_pk, review_pk):
    form = Comment()
    form.content = request.GET.get('inputText')
    form.user = request.user
    form.review = Review.objects.get(pk=review_pk)
    form.save()
    # 시간 양식 설정
    day_tmp = list(map(int, str(form.created_at.date()).split('-')))
    day_tmp.extend(list(map(int, str(form.created_at.time())[:5].split(':'))))
    print(day_tmp)
    day_tmp[3] += 9

    if day_tmp[3] >= 12:
        amPm = '오후'
        if day_tmp[3] != 12:
            day_tmp[3] -= 12
    else:
        amPm = '오전'

    new_time = str(day_tmp[0]) + '년 ' + str(day_tmp[1]) + '월 ' + str(day_tmp[2]) + '일 '
    new_time += str(day_tmp[3]) + ':' + str(day_tmp[4]) + ' ' + amPm
    print(new_time)

    new_comment = {
        'user': form.user.username,
        'content': form.content,
        'user_img': form.user.image.url,
        'created': new_time
    }
    data = {
        'new_comment': new_comment,
        'comment_pk': form.pk,
    }
    return JsonResponse(data)