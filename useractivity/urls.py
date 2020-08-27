from django.urls import path
from useractivity.views import UserActivityView

app_name = 'useractivity'

urlpatterns = [
	path('', UserActivityView.as_view())
]