from django.contrib import admin
from book.models import Books, BookDetails

# Register your models here.
admin.site.register(Books)
admin.site.register(BookDetails)
