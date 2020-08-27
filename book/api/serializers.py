from rest_framework import serializers
from book.models import BookDetails, Books


# Books Detials
# ------------------------------------------------
class BookDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookDetails
        fields = '__all__'

# Books
# ------------------------------------------------
class BooksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Books
        fields = '__all__'