from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from genre.models import Genre
from genre.api.serializers import GenreSerializer

# Create your views here.
# Genre        
# ------------------------------------------------
class GenreView(APIView):

    def get(self, request):
        genre_list = Genre.objects.all()
        serialzer = GenreSerializer(genre_list, context={"request": request}, many=True)
        return Response(serialzer.data)

    def post(self, request):
        serialzer = GenreSerializer(data=request.data, context={"request": request})
        if serialzer.is_valid():
            serialzer.save()
            return JsonResponse(serialzer.data, status = status.HTTP_201_CREATED)
        return JsonResponse(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)