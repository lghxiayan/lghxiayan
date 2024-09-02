from django.urls import path
from . import views

app_name = 'hg_info'

urlpatterns = [
    path('', views.index, name='index'),
    path('publish', views.info_publish, name='info_publish'),
    path('detail/<int:info_id>', views.info_detail, name='info_detail'),
    path('comment/pub', views.info_comment, name='info_comment'),
    path('search', views.info_search, name='info_search'),
]
