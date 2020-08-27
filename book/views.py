from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from book.models import BookDetails, Books
from book.api.serializers import BookDetailsSerializer, BooksSerializer

# Create your views here.
# Books Detials
# -----------------------------------------------
class BookDetailsView(APIView):

    def get(self, request):
        book_details_list = BookDetails.objects.all()
        serialzer = BookDetailsSerializer(book_details_list, many=True)
        return Response(serialzer.data)

    def post(self, request):
        serialzer = BookDetailsSerializer(data=request.data)
        if serialzer.is_valid():
            serialzer.save()
            return JsonResponse(serialzer.data, status = status.HTTP_201_CREATED)
        return JsonResponse(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)

# Books        
# ------------------------------------------------
class BooksView(APIView):

    def get(self, request):
        book_list = Books.objects.all()
        serialzer = BooksSerializer(book_list, many=True)
        return Response(serialzer.data)

    def post(self, request):
        serialzer = BooksSerializer(data=request.data)
        if serialzer.is_valid():
            serialzer.save()
            return JsonResponse(serialzer.data, status = status.HTTP_201_CREATED)
        return JsonResponse(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)