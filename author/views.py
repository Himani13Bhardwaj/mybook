from rest_framework.pagination import (
    PageNumberPagination,
    LimitOffsetPagination,
)
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from author.models import Author
from author.api.serializers import AuthorSerializer, AuthorProfileSerializer
from tools.pagination import StandardResultsSetPagination

# Create your views here.
# Author
# http://127.0.0.1:8000/api/authors/?limit=10&offset=10&page=1
# -----------------------------------------------
class AuthorView(ListAPIView):
    queryset = Author.objects.all().order_by('id')
    serializer_class = AuthorSerializer
    pagination_class = StandardResultsSetPagination

    def get(self, request, *args, **kwargs):
        StandardResultsSetPagination.page_size=10
        serializer = AuthorSerializer(Author.objects.all().order_by('id'), context={"request": request}, many=True)
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)


class AuthorProfileView(APIView):
    # def get(self, request):
    #     author_list = Author.objects.all()
    #     serialzer = AuthorSerializer(author_list, many=True)
    #     return Response(serialzer.data)

    # def post(self, request):
    #     serialzer = AuthorProfileSerializer(data=request.data)
    #     if serialzer.is_valid():
    #         #serialzer.save()
    #         return JsonResponse(serialzer.data, status = status.HTTP_201_CREATED)
    #     return JsonResponse(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        data = AuthorSerializer(Author.objects.all(), context={"request": request}, many=True).data
        return Response(data)

    def post(self, request):
        data = AuthorSerializer(Author.objects.get(id=request.data.get('author')), context={"request": request}).data
        return Response(data)
