from django.urls import path
from author.views import AuthorView

app_name = 'author'

urlpatterns = [
	path('', AuthorView.as_view())
]