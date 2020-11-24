"""bookhunt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
	# REST-framework
    path('api/account/', include('account.urls', 'account_api')),
    path('api/genres/', include('genre.urls', 'genre_api')),
    path('api/authors/', include('author.urls', 'author_api')),
    path('api/book/', include('book.urls', 'book_api')),
    path('api/comments/', include('comment.urls', 'comment_api')),
    path('api/userCollection/', include('usercollection.urls', 'usercollection_api')),
    path('api/userActivity/', include('useractivity.urls', 'useractivity_api')),
    path('api/userProfile/', include('userprofile.urls', 'userprofile_api')),
    path('api/sliders/', include('sliders.urls', 'sliders_api')),
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
