from django.urls import path
from book.views import BookDetailsView, BooksView

app_name = 'book'

urlpatterns = [
	path('bookDetails', BookDetailsView.as_view()),
    path('', BooksView.as_view()),
]