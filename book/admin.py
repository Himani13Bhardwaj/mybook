from django.contrib import admin
from book.models import Books, BookDetails, Chapter


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'book_name', 'chapters')
# Register your models here.
admin.site.register(Books, BookAdmin)
admin.site.register(BookDetails)
admin.site.register(Chapter)
