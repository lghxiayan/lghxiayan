from django.urls import path
from book import views

app_name = 'book'

urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.add_book, name='add_book'),
    path('add_article', views.add_article, name='add_article'),
    path('query', views.query_book, name='query_book'),
    path('order', views.order_book, name='order_book'),
    path('update', views.update_book, name='update_book'),
    path('delete', views.delete_book, name='delete_book'),
    # path('', views.book_detail_path, name='book_detail_path')
    path('detail/<int:book_id>', views.book_detail_path, name='book_detail_path')
]
