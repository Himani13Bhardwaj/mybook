from django.db import models

# Create your models here.
class Author(models.Model):
    
    author_name             = models.CharField(max_length=500)
    book_count              = models.IntegerField
    app_id                  = models.BigIntegerField

    def __str__(self):
        return self.author_name