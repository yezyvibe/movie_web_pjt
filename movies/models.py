from django.db import models
from django.conf import settings

class Genre(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=300)
    original_title = models.CharField(max_length=300, default='')
    release_date = models.DateField()
    popularity = models.FloatField()
    vote_count = models.IntegerField(default=0)
    vote_average = models.FloatField(default=0)
    adult = models.BooleanField(default=False)
    overview = models.TextField()
    original_language = models.CharField(max_length=10, default='')
    poster_path = models.CharField(max_length=100)
    backdrop_path = models.CharField(max_length=100, default='')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies', default='')
    genres = models.ManyToManyField(Genre, related_name='movies', default='')

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='my_reviews')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    rank = models.IntegerField(default=1)
    spoiler = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


