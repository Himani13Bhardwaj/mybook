from django.db import models
from book.models import Books
from account.models import Account
# Create your models here.
class Comments(models.Model):
    
    comment                 = models.CharField(max_length=500)
    book_id                 = models.ForeignKey(Books, related_name='comments', on_delete=models.CASCADE, default=1)
    user_id                 = models.ForeignKey(Account, on_delete=models.CASCADE, default=1)
    app_id                  = models.BigIntegerField

    def __str__(self):
        return self.comment  