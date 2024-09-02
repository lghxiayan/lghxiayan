from django.urls import path
from . import views

urlpatterns = [
    path('avg', views.avg_view, name='avg_view'),
    path('', views.index, name='index'),
    path('register', views.register_view, name='register_view')
]
