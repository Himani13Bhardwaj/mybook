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
        user_collection_list = UserCollection.objects.all()
        serialzer = UserCollectionSerializer(user_collection_list, many=True)
        return Response(serialzer.data)

    # def post(self, request):
    #     serialzer = UserCollectionSerializer(data=request.data)
    #     if serialzer.is_valid():
    #         serialzer.save()
    #         return JsonResponse(serialzer.data, status = status.HTTP_201_CREATED)
    #     return JsonResponse(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        userid = request.data.get('userid')
        useremail = request.data.get('useremail')
        try:
            booksid = UserCollection.objects.filter(user__id=userid).values_list('book_id', flat=True)    
        except UserCollection.DoesNotExist:
            booksid = []
        books = Books.objects.filter(id__in=booksid)
        class apibookserializer(BooksSerializer):
            author = serializers.CharField(source='author.author_name')
            genre = serializers.CharField(source='genre.genre_name')
        apibookserializer.Meta.fields.extend(['author', 'genre', 'ranking'])
        data = apibookserializer(books, many=True).data
        return Response(data)