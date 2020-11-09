from django.urls import path
from book.views import *

app_name = 'book'

urlpatterns = [
	path('bookDetails/<int:pk>', BookDetailsView.as_view()),
    path('', BooksView.as_view()),
    # path('search/', BooksSearchView.as_view()),
    path('bookread/', BookReadView.as_view()),
    path('bookinfo/', BookInfoView.as_view()),
    path('upvote/', upvote),
    path('downvote/', downvote),
    path('comment/', comment),
    path('search/', search),
    path('latest/', LatestView.as_view()),
]