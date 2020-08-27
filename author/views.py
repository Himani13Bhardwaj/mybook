from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from author.models import Author
from author.api.serializers import AuthorSerializer

# Create your views here.
# Author
# -----------------------------------------------
class AuthorView(APIView):

    def get(self, request):
        author_list = Author.objects.all()
        serialzer = AuthorSerializer(author_list, many=True)
        return Response(serialzer.data)

    def post(self, request):
        serialzer = AuthorSerializer(data=request.data)
        if serialzer.is_valid():
            serialzer.save()
            return JsonResponse(serialzer.data, status = status.HTTP_201_CREATED)
        return JsonResponse(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)