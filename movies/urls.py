from django.urls import path
from . import views

app_name = "movies"

urlpatterns=[
    path('', views.home, name="home"),
    path('search/', views.search, name="search"),
    path('index/', views.index, name="index"),
    path('create/', views.movie_create, name="movie_create"),
    path('<int:movie_pk>/update/', views.movie_update, name="movie_update"),
    path('<int:movie_pk>/delete/', views.movie_delete, name="movie_delete"),
    path('<int:movie_pk>/', views.detail, name="detail"),
    path('<int:movie_pk>/like/', views.like, name="like"),
    path('<int:movie_pk>/review_create', views.review_create, name="review_create"),
    path('<int:movie_pk>/<int:review_pk>/', views.review_detail, name="review_detail"),
    path('<int:movie_pk>/<int:review_pk>/review_delete/', views.review_delete, name="review_delete"),
    path('<int:movie_pk>/<int:review_pk>/review_update/', views.review_update, name="review_update"),
    path('<int:movie_pk>/<int:review_pk>/<int:comment_pk>/', views.comment_delete, name="comment_delete"),
    path('<int:movie_pk>/<int:review_pk>/comment_create/', views.comment_create, name="comment_create")
]