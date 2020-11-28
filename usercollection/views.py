from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from book.models import Books
from usercollection.models import UserCollection
from usercollection.api.serializers import UserCollectionSerializer
from book.api.serializers import BooksSerializer

# Create your views here.
# User Collection     
# ------------------------------------------------
class UserCollectionView(APIView):
    
    model = UserCollection
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        try:
            booksid = UserCollection.objects.filter(user__id=request.user.id).values_list('book_id', flat=True)    
        except UserCollection.DoesNotExist:
            booksid = []
        books = Books.objects.filter(id__in=booksid)
        class apibookserializer(BooksSerializer):
            author = serializers.CharField(source='author.author_name')
            genre = serializers.CharField(source='genre.genre_name')
        apibookserializer.Meta.fields.extend(['author', 'genre', 'ranking'])
        data = apibookserializer(books, context={"request": request}, many=True).data 
        return Response(data)
    

    def post(self, request):
        userid = request.user.id
        useremail = request.user.email
        print(userid, useremail)
        try:
            booksid = UserCollection.objects.filter(user__id=userid).values_list('book_id', flat=True)    
        except UserCollection.DoesNotExist:
            booksid = []
        books = Books.objects.filter(id__in=booksid)
        class apibookserializer(BooksSerializer):
            author = serializers.CharField(source='author.author_name')
            genre = serializers.CharField(source='genre.genre_name')
        apibookserializer.Meta.fields.extend(['author', 'genre', 'ranking'])
        data = apibookserializer(books, context={"request": request}, many=True).data
        return Response(data)