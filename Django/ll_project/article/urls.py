from django.urls import path

from article import views

app_name = 'article'

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.author, name='author'),
    path('list/<int:auth_id>', views.article_list, name='article_list'),
]
