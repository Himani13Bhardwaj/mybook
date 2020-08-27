from django.urls import path
from usercollection.views import UserCollectionView

app_name = 'usercollection'

urlpatterns = [
	path('', UserCollectionView.as_view())
]