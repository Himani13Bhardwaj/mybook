from django.urls import path
from sliders.views import SliderView

app_name = 'sliders'

urlpatterns = [
	path('', SliderView.as_view()),
]