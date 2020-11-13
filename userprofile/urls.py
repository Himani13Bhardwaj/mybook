from django.urls import path
from userprofile.views import UserProfileView, AddCoinsView

app_name = 'userprofile'

urlpatterns = [
	path('', UserProfileView.as_view()),
	path('claim/', AddCoinsView.as_view())
]