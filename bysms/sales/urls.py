from django.urls import path

from sales.views import list_customers, listorders

urlpatterns = [
    path('orders/', listorders),
    path('customers/', list_customers),
    # path('orders1/', listorders1),
    # path('orders2/', listorders2),
    # path('orders3/', listorders3),
]
