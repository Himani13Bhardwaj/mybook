from django.db import models
from book.models import Books
from account.models import Account

# Create your models here.
class UserCollection(models.Model):

    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    book_id                 = models.ForeignKey(Books, on_delete=models.CASCADE, default=1)
    logged_in_time          = models.TimeField(auto_now=True)

    def __str__(self):
        return str(str(self.user)+' | '+str(self.book_id))