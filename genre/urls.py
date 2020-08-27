from django.urls import path
from genre.views import GenreView

app_name = 'genre'

urlpatterns = [
	path('', GenreView.as_view())
]