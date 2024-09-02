from django.urls import path

from pizzas import views

app_name = 'pizzas'

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.pizzas, name='pizzas'),
    path('list/<int:pizza_id>/', views.pizza_details, name='pizza'),
]
