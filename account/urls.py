from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('customer/<str:', views.customers),
    path('products/', views.products),
    path('create_customer/', views.createCustomer, name='createCustomer'),


]
