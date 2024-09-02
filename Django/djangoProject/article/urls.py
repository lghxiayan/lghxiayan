from django.urls import path
from . import views

app_name = 'article'

urlpatterns = [
    path('add/', views.add_article, name='add_article'),
    path('one/', views.one_to_many, name='one_article'),
    path('q1/', views.query_1, name='query_1'),
    path('q4/', views.query_4, name='query_4'),
]
