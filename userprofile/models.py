from django.db import models
from useractivity.models import UserActivity
from account.models import Account

# Create your models here.
class UserProfile(models.Model):

    coins                   = models.IntegerField(default=0)
    logged_date             = models.DateField(auto_now=True)
    user_profile            = models.DateField(auto_now=True)
    user_id                 = models.ForeignKey(Account, on_delete=models.CASCADE, default=1)
    # user_activity_id        = models.ForeignKey(UserActivity, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.user_id)