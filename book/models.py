from django.db import models
from enumchoicefield import ChoiceEnum, EnumChoiceField
from author.models import Author
from genre.models import Genre

# Create your models here.

class State(ChoiceEnum):
    locked       = "Locked"
    unlocked     = "Un-Locked"
    free         = "Free"
    bonus        = "Bonus"

class BookDetails(models.Model):
    
    view                    = models.CharField(max_length=100)
    upvote                  = models.CharField(max_length=100)
    downvote                = models.CharField(max_length=100)

    def __str__(self):
        return self.view

    
class Books(models.Model):
    book_name               = models.CharField(max_length=254)
    book_cover_url          = models.ImageField(blank=False, null=False)
    chapters                = models.IntegerField
    view                    = models.CharField(max_length=100)
    published_time          = models.DateField(auto_now=True)
    user_count              = models.CharField(max_length=100)
    ranking                 = models.CharField(max_length=100)
    book_brief_info         = models.CharField(max_length=100)
    genre                   = models.ForeignKey(Genre, on_delete=models.CASCADE, default=1)
    # author                  = models.ForeignKey(Author, on_delete=models.CASCADE, default=1)
    author                  = models.ForeignKey(Author, related_name='books' ,on_delete=models.CASCADE, default=1)
    book_details            = models.ForeignKey(BookDetails, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.book_name

class Chapter(models.Model):

    chapter_no              = models.PositiveIntegerField(null=True, blank=True)
    chapter_name            = models.CharField(max_length=100)
    chapter_url             = models.FileField(blank=False, null=False)
    state                   = EnumChoiceField(enum_class=State , default=State.free)
    book_id                 = models.ForeignKey(Books, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.chapter_name