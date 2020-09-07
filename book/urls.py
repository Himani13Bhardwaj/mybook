from django.urls import path
from book.views import *

app_name = 'book'

urlpatterns = [
	path('bookDetails/<int:pk>', BookDetailsView.as_view()),
    path('', BooksView.as_view()),
    path('search/', BooksSearchView.as_view()),
    path('bookread/', BookReadView.as_view())
]