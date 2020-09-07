from django.urls import path
from author.views import AuthorView, AuthorProfileView

app_name = 'author'

urlpatterns = [
	path('', AuthorView.as_view()),
	path('profile/', AuthorProfileView.as_view())
]