from django.urls import path
from . import views

app_name="accounts"
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('update/', views.update, name='update'),
    path('delete/', views.delete, name='delete'),
    path('login/', views.login, name ='login'),
    path('logout/', views.logout, name='logout'),
    path('<username>/', views.profile, name='profile'),
    path('<username>/follow/', views.follow, name='follow'),
    path('<username>/like_movies/', views.like_movies, name='like_movies'),
    path('<username>/my_reviews/', views.my_reviews, name='my_reviews'),
]