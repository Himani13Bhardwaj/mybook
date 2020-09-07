from rest_framework import serializers
from author.models import Author

class AuthorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Author
        fields = ['id', 'author_name']

class AuthorProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = '__all__'