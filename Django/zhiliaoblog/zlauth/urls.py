from django.urls import path
from . import views

app_name = 'zlauth'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('login/', views.zllogin, name='login'),
    path('logout/', views.zllogout, name='logout'),
    path('register/', views.register, name='register'),
    path('captcha/', views.send_email_captcha, name='send_email_captcha'),
]
