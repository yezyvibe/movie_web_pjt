from django import forms
from .models import Review, Comment, Movie

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'content', 'rank', 'spoiler']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class MovieCreationForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title','release_date','popularity','poster_path','backdrop_path','overview', 'genres']
        
        # genres(manytomany연결) 필드 넣기