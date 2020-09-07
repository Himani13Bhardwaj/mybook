from django.db.models import Q
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)

from rest_framework.pagination import (
    PageNumberPagination,
    LimitOffsetPagination,
)

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from book.models import *
from book.api.serializers import *

# Create your views here.
# Books Detials
# -----------------------------------------------
class BookDetailsView(RetrieveAPIView):

    queryset = BookDetails.objects.all()
    serializer_class = BookDetailsSerializer
    lookup_field = 'pk'

    def post(self, request):
        serialzer = BookDetailsSerializer(data=request.data)
        if serialzer.is_valid():
            serialzer.save()
            return JsonResponse(serialzer.data, status = status.HTTP_201_CREATED)
        return JsonResponse(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)

# Books        
# http://127.0.0.1:8000/api/book/?limit=10&offset=0&page=1
# ------------------------------------------------
class BooksView(ListAPIView):

    queryset = Books.objects.all().order_by('id')
    serializer_class = BooksSerializer
    pagination_class = LimitOffsetPagination



class BooksSearchView(ListAPIView):
    
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    filter_backends = [SearchFilter]
    search_fields = ['book_name', 'author__author_name']


class BookReadView(APIView):
    model = Chapter
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    # Type: POST request
    # Parameter= bookname, bookid, chapter, userid
    # Header = appid, cookieid
    # Algorithm:
    # If userid is there: // apply authentication class
    #     If check bookname and book id are valid
    #         If chapter is available and chapter is free
    #             add this activity in useractiving
    #             Return chapter of the book
    #         Else:
    #             If check available coins with respective to user if == 20:
    #                   Update the user accound with -20
    #                    Set the state of the chapter with respect to book = unlock by entering this activity in useractiving
    #                    do entry in useractivity
    #                 Return chapter of the book
    #             Else:
    #                 Return kindly must collect the coins of the books
    #     Else:
    #         “kindly connect with the right book”
    # Else:
    #     “kindly login first”

    def post(self, request):
        print(request.data)
        userid = request.data.userid
        bookid = request.data.bookid
        bookname = request.data.bookname
        chapter_no = request.data.chapter

        user = Account.objects.get(pk = userid)
        if user is not None:
            book = Books.object.get(id=bookid)
            if book.book_name == bookname:
                chapter = Chapter.objects.get(book_id, chapter_no)
                if chapter.state == 'Free':
                    # update the user activity
                    return Response(chapter)
                else:
                    return Response('')
    #                If check available coins with respective to user if == 20:
    #                   Update the user accound with -20
    #                    Set the state of the chapter with respect to book = unlock
    #                    do entry in useractivity
    #                   Return chapter of the book
    #                 Else:
    #                    Return kindly must collect the coins of the books
            return  Response("kindly check the right book")
        return Response("Kindly register yourself first")
