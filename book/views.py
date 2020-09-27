from django.db.models import Q
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)

from rest_framework.pagination import (
    PageNumberPagination,
    LimitOffsetPagination,
)
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
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
from tools.pagination import StandardResultsSetPagination
from account.models import Account
from comment.models import Comments
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
# class BooksView(ListAPIView):

#     queryset = Books.objects.all().order_by('id')
#     serializer_class = BooksSerializer
    # pagination_class = LimitOffsetPagination

class BooksView(APIView):

    pagination_class = StandardResultsSetPagination
    
    def get(self, request):

        paginator = Paginator(Books.objects.all(), 20)
        page = request.query_params.get('page')
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
        except EmptyPage:
            books = paginator.page(paginator.num_pages)
        BooksSerializer.Meta.fields = ['id', 'book_name', 'book_cover_url']
        data = BooksSerializer(books, many=True).data
        return Response(data)


class BookInfoView(APIView):
    # api/book/bookinfo/
    def post(self, request):
        books = Books.objects.filter(id=request.data.get('bookid'),
                                book_name=request.data.get('bookname'))
        class BookSerializer(BooksSerializer):
            upvote = serializers.CharField(source='book_details.upvote')
            downvote = serializers.CharField(source='book_details.downvote')
            comments = serializers.StringRelatedField(many=True)
            author = serializers.CharField(source='author.author_name')
        BookSerializer.Meta.fields = ['id', 'book_name', 'book_cover_url', 'view', 'upvote', 'downvote', 'book_brief_info', 'genre', 'author', 'ranking', 'comments']
        data = BookSerializer(books, many=True).data
        return Response(data)

# class BooksSearchView(ListAPIView):
    
#     queryset = Books.objects.all()
#     serializer_class = BooksSerializer
#     filter_backends = [SearchFilter]
#     search_fields = ['book_name', 'author__author_name']


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
        userid = request.data.get('userid')
        bookid = request.data.get('bookid')
        bookname = request.data.get('bookname')
        # chapter_no = request.data.get('chapter')

        user = Account.objects.get(pk = userid)
        if user is not None:
            book = Books.objects.get(id=bookid)
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


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
# api/book/upvote/
def upvote(request):
    '''
    increases the upvote by 1
    '''
    bookname = request.data.get('bookname')
    bookid = request.data.get('bookid')
    book = Books.objects.select_related('book_details').get(id=bookid, book_name=bookname)
    print(book)
    bookdetail = BookDetails.objects.get(id=book.book_details.id)
    upvote_count = int(bookdetail.upvote) + 1
    bookdetail.upvote = upvote_count
    bookdetail.save()
    book = Books.objects.get(book_name=bookname, id=bookid)
    class BookSerializer(BooksSerializer):
            upvote = serializers.CharField(source='book_details.upvote')
            downvote = serializers.CharField(source='book_details.downvote')
            comments = serializers.StringRelatedField(many=True)
            author = serializers.CharField(source='author.author_name')
    BookSerializer.Meta.fields = ['id', 'book_name', 'book_cover_url', 'view', 'upvote', 'downvote', 'book_brief_info', 'genre', 'author', 'ranking', 'comments']
    data = BookSerializer(book).data
    return Response(data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
# api/book/upvote/
def downvote(request):
    '''
    increases the upvote by 1
    '''
    bookname = request.data.get('bookname')
    bookid = request.data.get('bookid')
    book = Books.objects.select_related('book_details').get(id=bookid, book_name=bookname)
    print(book)
    bookdetail = BookDetails.objects.get(id=book.book_details.id)
    downvote_count = int(bookdetail.downvote) + 1
    bookdetail.downvote = downvote_count
    bookdetail.save()
    book = Books.objects.get(book_name=bookname, id=bookid)
    class BookSerializer(BooksSerializer):
            upvote = serializers.CharField(source='book_details.upvote')
            downvote = serializers.CharField(source='book_details.downvote')
            comments = serializers.StringRelatedField(many=True)
            author = serializers.CharField(source='author.author_name')
    BookSerializer.Meta.fields = ['id', 'book_name', 'book_cover_url', 'view', 'upvote', 'downvote', 'book_brief_info', 'genre', 'author', 'ranking', 'comments']
    data = BookSerializer(book).data
    return Response(data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
# api/book/upvote/
def comment(request):
    '''
    increases the upvote by 1
    '''
    bookname = request.data.get('bookname')
    bookid = request.data.get('bookid')
    comment = request.data.get('comment')
    book = Books.objects.get(book_name=bookname, id=bookid)
    Comments.objects.create(book_id=book, user_id=request.user, comment=comment)
    class BookSerializer(BooksSerializer):
            upvote = serializers.CharField(source='book_details.upvote')
            downvote = serializers.CharField(source='book_details.downvote')
            comments = serializers.StringRelatedField(many=True)
            author = serializers.CharField(source='author.author_name')
    BookSerializer.Meta.fields = ['id', 'book_name', 'book_cover_url', 'view', 'upvote', 'downvote', 'book_brief_info', 'genre', 'author', 'ranking', 'comments']
    data = BookSerializer(book).data
    return Response(data)


@api_view(['POST'])
def search(request):
    bookname = request.data.get('bookname')
    authorname = request.data.get('authorname')
    if bookname:
        data = BooksSerializer(Books.objects.filter(book_name__icontains = bookname), many=True).data
    elif authorname:
        authors = Author.objects.filter(author_name__icontains = authorname).values_list('id', flat=True)
        for item in authors: print(item)
        BooksSerializer.Meta.fields.extend(['author', 'ranking'])
        data = BooksSerializer(Books.objects.filter(author__id__in = authors), many=True).data
        print(authors)
    return Response(data)