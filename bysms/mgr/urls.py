from django.urls import path

from mgr import customer, sing_in_out

urlpatterns = [
    path('customers', customer.dispatcher),
    path('signin', sing_in_out.signin),
    path('signout', sing_in_out.signout),
]
