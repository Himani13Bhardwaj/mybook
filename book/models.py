from django.db import models
from author.models import Author
from genre.models import Genre

# Create your models here.
class BookDetails(models.Model):
    
    view                    = models.CharField(max_length=100)
    upvote                  = models.CharField(max_length=100)
    downvote                = models.CharField(max_length=100)

    
class Books(models.Model):
    
    book_name               = models.CharField(max_length=254)
    book_cover_url          = models.URLField(max_length=500)
    chapters                = models.IntegerField
    book_url                = models.URLField(max_length=500)
    view                    = models.CharField(max_length=100)
    published_time          = models.DateField(auto_now=True)
    user_count              = models.CharField(max_length=100)
    ranking                 = models.CharField(max_length=100)
    state                   = models.CharField(max_length=100)
    book_brief_info         = models.CharField(max_length=100)
    genre_id                = models.ForeignKey(Genre, on_delete=models.CASCADE, default=1)
    author_id               = models.ForeignKey(Author, on_delete=models.CASCADE, default=1)
    book_details_id         = models.ForeignKey(BookDetails, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.book_name
