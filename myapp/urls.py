from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.loginin, name='login'),
    path('balance/', views.balance, name='balance'),
    path('deposit/', views.deposit, name='deposit'),
    path('order/', views.order_request, name='order_request'),
    path('payment/', views.payment_request, name='payment_request'),
    path('refund/', views.refund, name='refund'),
    path('search/', views.search, name='search'),
    path('login_Failed/', views.Login_Failed, name='Login_Failed')
]
