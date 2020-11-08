from django.contrib import admin
from genre.models import Genre

# Register your models here.
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['genre_name', 'app_id', 'genre_img']
