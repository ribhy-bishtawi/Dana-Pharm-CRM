from http import client
import imp
from multiprocessing import context
from unittest import result
from django.shortcuts import render
from account.IndexClient import IndexClient

from account.fire_store import FirebaseClient
from firebase_admin import auth
from account.orderClient import OrderClient

from account.user_client import UserClient


def home(request):
    userClient = UserClient()
    users = userClient.all()

    orderClient = OrderClient()
    orders = orderClient.all()
    totalOrders = len(orders)

    context = {'users': users, 'totalOrders': totalOrders, 'orders': orders}
    return render(request, 'account/dashboard.html', context)


def products(request):
    # productClinet = FirebaseClient("Product")

    # products = clinet.all()
    return render(request, 'account/products.html', {'products': products})


def customers(request, docId):
    userClient = UserClient()
    user = userClient.get_by_id(docId)
    return render(request, 'account/customers.html')


def createCustomer(request):
    if(request.method == 'POST'):
        userClient = UserClient()
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        user = auth.create_user(email=email, password=password)

        data = {'name': name, 'email': email,
                'password': password, 'oredersCount': '0'}
        userClient.createWithDocID(data, user.uid)

    context = {}
    return render(request, 'account/createCustomer.html', context)
