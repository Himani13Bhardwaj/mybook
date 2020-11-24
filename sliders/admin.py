from django.contrib import admin
from sliders.models import Sliders
# Register your models here.

# admin.site.register(Sliders)
@admin.register(Sliders)
class SlidersAdmin(admin.ModelAdmin):
	list_display = ['slider_id', 'slider_url', 'type_slider']
