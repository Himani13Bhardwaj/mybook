from rest_framework import serializers
from book.models import BookDetails, Books, Chapter
from genre.api.serializers import *
from author.api.serializers import *

# Books Detials
# ------------------------------------------------
class BookDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookDetails
        fields = '__all__'

# Books
# ------------------------------------------------
# class BooksSerializer(serializers.ModelSerializer):

#     genre = GenreSerializer(read_only=True)
#     author = AuthorSerializer(read_only=True)
#     book_details = BookDetailsSerializer(read_only=True)

#     class Meta:
#         model = Books
#         fields = '__all__'

class BooksSerializer(serializers.ModelSerializer):
    # upvote = serializers.CharField(source='book_details.upvote')
    # downvote = serializers.CharField(source='book_details.downvote')
    # comments = serializers.StringRelatedField(many=True)
    # author = serializers.CharField(source='author.author_name')

    class Meta:
        model = Books
        fields = ['id', 'book_name', 'book_cover_url']

# Chapter
# ------------------------------------------------
class ChapterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chapter
        fields = '__all__'