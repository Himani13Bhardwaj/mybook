from rest_framework import serializers
from comment.api.serializers import CommentsSerializer
from book.api.serializers import BooksSerializer
from book.models import Books


class BookLatestSerializer(BooksSerializer):
    # upvote = serializers.CharField(source='book_details.upvote')
    # downvote = serializers.CharField(source='book_details.downvote')
    # comments = CommentsSerializer(many=True)
    # author = serializers.CharField(source='author.author_name')

    class Meta:
        model = Books
        fields = ['id', 'book_name', 'book_cover_url']