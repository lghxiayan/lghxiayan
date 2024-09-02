"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include, reverse
from django.shortcuts import HttpResponse
from django.views.static import serve

from home import views as home_views
from django.conf.urls.static import static
from django.conf import settings

# def index(request):
#     print(reverse('book:book_detail_query_string'))
#     return HttpResponse('Hello World')


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', home_views.index, name='index'),
    path('book/', include('book.urls')),
    path('movie/', include('movie.urls')),
    path('article/', include('article.urls')),
    path('if', home_views.if_view, name='if'),
    path('for', home_views.for_view, name='for'),
    path('with', home_views.with_view, name='with'),
    path('url', home_views.url_view, name='url'),
    path('filter', home_views.filter_view, name='filter'),
    path('new_index', home_views.new_index, name='new_index'),
    path('sta', home_views.static_view, name='static_view'),
    path('front/', include('front.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
