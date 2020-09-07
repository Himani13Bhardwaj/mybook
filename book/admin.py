from django.contrib import admin
from book.models import Books, BookDetails, Chapter

# Register your models here.
admin.site.register(Books)
admin.site.register(BookDetails)
admin.site.register(Chapter)
