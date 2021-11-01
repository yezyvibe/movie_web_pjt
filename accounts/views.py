from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
# from django.contrib import messages

# 팔로우 팔로잉 비동기
from django.http import JsonResponse
# Create your views here.

def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:index')
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect(request.GET.get('next') or 'movies:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form':form
    }
    return render(request, 'accounts/form.html', context)

@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()
            return redirect('accounts:profile', user.username)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form':form
    }
    return render(request, 'accounts/form.html', context)

@login_required
def delete(request):
    request.user.delete()
    return redirect('movies:index')

def login(request):
    if request.user.is_authenticated:
        return redirect(request.GET.get('next') or 'movies:index')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'movies:index')
    else:
        form = AuthenticationForm()
    context = {
        'form':form
    }
    return render(request, 'accounts/login.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('movies:index')

def profile(request, username):
    User = get_user_model()
    profile_user = get_object_or_404(User, username=username)
    if profile_user.image == '':
        profile_user.image = 'profile_img.png' 
    context = {
        'profile_user': profile_user
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def follow(request, username):
    User = get_user_model()
    user = get_object_or_404(User, username=username)
    if request.user != user:
        if user.followers.filter(pk=request.user.pk).exists():
            user.followers.remove(request.user)
            status = False
        else:
            user.followers.add(request.user)
            status = True
        data = {
            'status': status,
            'followers_count': user.followers.count(),
            'followings_count': user.followings.count()
        }
        return JsonResponse(data)

def like_movies(request, username):
    User = get_user_model()
    user = get_object_or_404(User, username=username)
    movies = user.like_movies.all()
    context = {
        'movies':movies,
        'profile_user': user,
    }
    return render(request, 'accounts/like_movies.html', context)

def my_reviews(request, username):
    User = get_user_model()
    user = get_object_or_404(User, username=username)
    reviews = user.my_reviews.all()
    context = {
        'reviews':reviews,
        'profile_user': user,
    }
    return render(request, 'accounts/my_reviews.html', context)