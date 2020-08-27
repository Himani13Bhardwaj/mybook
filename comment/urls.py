from django.urls import path
from comment.views import CommentsView

app_name = 'comment'

urlpatterns = [
	path('', CommentsView.as_view())
]