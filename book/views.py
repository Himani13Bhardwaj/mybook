from django_filters.rest_framework import DjangoFilterBackend
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
from usercollection.models import UserCollection
from useractivity.models import UserActivity
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
    filterset_fields = ['genre']
    filter_backends = [DjangoFilterBackend]

    def get(self, request):

        def filter_queryset(queryset):
            for backend in list(self.filter_backends):
                queryset = backend().filter_queryset(self.request, queryset, self)
            return queryset

        paginator = Paginator(filter_queryset(Books.objects.filter()), 20)
        page = request.query_params.get('page')
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = []
        except EmptyPage:
            books = []
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
    
    def searchUser(self, _id):
        user = Account.objects.get(pk = _id)
        if user is not None:
            return True
        return False

    def searchBook(self, _id, _name):
        try:
            book = Books.objects.get(id=_id)
            if book.book_name == _name:
                return True
            return False
        except Books.DoesNotExist:
            return False

    def searchBookChapter(self, _book_id, _chapter):
        try:
            _chapter = Chapter.objects.get(book_id=_book_id, chapter_no=_chapter)
            return _chapter
        except Chapter.DoesNotExist:
            return None

    def searchBookInUserActivity(self, _id, _book_id, _chapter):
        try:
            useractivity = UserActivity.objects.get(user_id=_id, book_id_id=_book_id, chapter= _chapter)
            return useractivity
        except UserActivity.DoesNotExist:
            return None
    
    def searchBookInUserCollection(self, _id, _book_id):
        try:
            _collection = UserCollection.objects.get(user_id=_id, book_id_id=_book_id)
            return True
        except UserCollection.DoesNotExist:
            return False
        
    def post(self, request):
        userid = request.data.get('userid')
        bookid = request.data.get('bookid')
        bookname = request.data.get('bookname')
        chapter_no = request.data.get('chapter')

        user = Account.objects.get(pk = userid)
        if BookReadView.searchUser(self, userid):
            if BookReadView.searchBook(self, bookid, bookname):
                _chapter = BookReadView.searchBookChapter(self, bookid, chapter_no)
                if _chapter is not None:
                    if not BookReadView.searchBookInUserCollection(self, request.user, bookid):
                        book = Books.objects.get(id=bookid)
                        UserCollection.objects.get_or_create(user=request.user, book_id=book)
                    chapter = ChapterSerializer(_chapter).data
                    if BookReadView.searchBookInUserActivity(self, request.user, bookid, chapter_no) is not None:
                        return Response(chapter)             
                    if chapter['state'] == 'free':
                        try:
                            user_act = UserActivity.objects.create(user_id=request.user, book_id_id=bookid)
                            user_act.unlocked_chapter = True
                            user_act.chapter = chapter_no
                            user_act.save()
                            return Response(chapter)  
                        except Exception:
                            return Response({'message': 'Server Issue.'})                                 
                    return Response({'message': 'To Unlock the new chapter, You have to earn coins.'})
                else:
                    return Response({'message': 'chapter doesnt exist'})
            else:
               return Response({'message': 'select the appropriate book'})
        else:
            return Response({'message': 'Please login first'})


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
    try:
        book = Books.objects.select_related('book_details').get(id=bookid, book_name=bookname)
    except Books.DoesNotExist:
        return Response('no book exists')
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
    try:
        book = Books.objects.select_related('book_details').get(id=bookid, book_name=bookname)
    except Books.DoesNotExist:
        return Response('no book exists')
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
    try:
        book = Books.objects.get(book_name=bookname, id=bookid)
    except Books.DoesNotExist:
        return Response('no book exists')
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


class LatestView(APIView):
    def get(self, request):
        data = dict()
        try:
            data['latest'] = BooksSerializer(Books.objects.order_by('published_time')[:5], many=True).data
            try:
                data['deals'] = BooksSerializer(Books.objects.order_by('ranking')[:5], many=True).data
            except Exception:
                data['deals'] = []
        except Exception:
            data['latest'] = []
        return Response(data)
