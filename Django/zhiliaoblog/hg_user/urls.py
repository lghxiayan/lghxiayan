from django.urls import path
from . import views

app_name = 'hg_user'

urlpatterns = [
    path('', views.hg_index, name='index'),
    path('login/', views.hg_login, name='login'),
    path('logout/', views.hg_logout, name='logout'),
    path('register/', views.hg_register, name='register'),
    path('captcha/', views.send_phone_captcha, name='send_phone_captcha'),
]
