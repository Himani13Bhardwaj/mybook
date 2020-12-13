from django.urls import path
from useractivity.views import UserActivityView, FeedbackView

app_name = 'useractivity'

urlpatterns = [
	path('', UserActivityView.as_view()),
	path('feedback', FeedbackView.as_view())
	# path('feedback', feedbackView.as_view())
]