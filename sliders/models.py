from django.db import models
from enumchoicefield import ChoiceEnum, EnumChoiceField
# Create your models here.
Image_Path = 'static/sliders'

class TypeState(ChoiceEnum):
    genre       = "Genre"
    author      = "Author"
    book        = "Book"
    latest      = "Best Deal"

class Sliders(models.Model):
    slider_id               = models.BigIntegerField
    slider_url              = models.ImageField(upload_to = Image_Path, default = '')
    type_slider             = EnumChoiceField(enum_class=TypeState , default=TypeState.book)

    def __str__(self):
        return str(self.type_slider)