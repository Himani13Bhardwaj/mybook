from django.db import models
from django_countries.fields import CountryField

# Create your models here.
class Author(models.Model):
    
    author_name             = models.CharField(max_length=500)
    book_count              = models.IntegerField
    app_id                  = models.BigIntegerField
    profilepicture          = models.ImageField(upload_to = 'static/profile', default = '')
    birth_date              = models.DateField('DOB', blank=True, null=True)
    hobbies                 = models.TextField(blank=True, null=True)
    nationality             = CountryField(blank_label='(select country)')

    def __str__(self):
        return self.author_name
    