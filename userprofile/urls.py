from django.urls import path
from userprofile.views import UserProfileView

app_name = 'userprofile'

urlpatterns = [
	path('', UserProfileView.as_view())
]