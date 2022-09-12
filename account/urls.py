from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('customer_orders/<str:docId>/',
         views.customersOrders, name='customerOrders'),
    path('products/', views.products, name='products'),
    path('create_customer/', views.createCustomer, name='createCustomer'),
    path('order_details/<str:docId>/', views.orderDetails, name='orderDetails'),
    path('login/', views.loginPage, name='loginPage'),
    path('logout/', views.logoutU, name='logout'),
    path('orders/', views.orders, name='orders'),
    path('update/<str:docId>/', views.updateOrder, name='updateOrder'),
    path('delete/<str:docId>/', views.deleteOrder, name='deleteOrder'),
    path('customers/', views.customers, name='customers'),
    path('add_product/', views.addProduct, name='addProduct'),
]
