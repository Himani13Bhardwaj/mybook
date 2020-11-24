from rest_framework import serializers
from author.models import Author
from book.api.serializers import BooksSerializer
# class AuthorSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Author
#         fields = ['id', 'author_name']

class AuthorProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):

    books = BooksSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'author_name', 'hobbies', 'profilepicture', 'books']
