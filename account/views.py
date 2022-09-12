import datetime
from http import client
import imp
from multiprocessing import context
from unittest import result
from django.shortcuts import redirect, render
from account import productClient
from account.IndexClient import IndexClient

from firebase_admin import auth
from account.orderClient import OrderClient
from account.user_client import UserClient
from account.productClient import ProductClient

from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url='loginPage')
def home(request):
    userClient = UserClient()
    orderdUsers = userClient.orderBy('name', 5)

    orderClient = OrderClient()
    orders = orderClient.all()
    orderdOrders = orderClient.orderBy('date', 4)
    totalOrders = len(orders)

    readyOrdersFilter = orderClient.filter('status', '==', 'تم التوصيل')
    readyOrdersQ = len(readyOrdersFilter)

    pendingOrdersFilter = orderClient.filter('status', '==', 'في الأنتظار')
    pendingOrdersQ = len(pendingOrdersFilter)

    context = {'customers': orderdUsers, 'totalOrders': totalOrders,
               'orders': orderdOrders, 'pendingOrdersQ': pendingOrdersQ, 'readyOrdersQ': readyOrdersQ}
    return render(request, 'account/dashboard.html', context)


@login_required(login_url='loginPage')
def products(request):
    productClient = ProductClient()
    products = productClient.all()

    if(request.method == 'POST'):
        query = request.POST.get('searchQuery')
        products = productClient.filter('name', '==', query.strip())

    p = Paginator(products, 10)
    page = request.GET.get('page')
    pagProducts = p.get_page(page)
    pageNum = 'd' * pagProducts.paginator.num_pages

    context = {'products': pagProducts, 'pageNum': pageNum}

    return render(request, 'account/products.html', context)


@login_required(login_url='loginPage')
def customersOrders(request, docId):
    userClient = UserClient()
    user = userClient.get_by_id(id=docId)

    orderClient = OrderClient()
    usersOrders = orderClient.filter('user_id', '==', docId.strip())
    userOrdersLen = len(usersOrders)

    context = {'user': user, 'orders': usersOrders,
               'userOrdersLen': userOrdersLen}
    return render(request, 'account/customersOrders.html', context)


@login_required(login_url='loginPage')
def orderDetails(request, docId):
    orderClient = OrderClient()
    usersOrdersDetail = orderClient.getItems(docId)

    context = {'orders': usersOrdersDetail}
    return render(request, 'account/orderDetails.html', context)


@login_required(login_url='loginPage')
def customers(request):
    userClient = UserClient()
    users = userClient.all()

    if(request.method == 'POST'):
        query = request.POST.get('searchQuery')
        users = userClient.filter('name', '==', query)
    p = Paginator(users, 10)
    page = request.GET.get('page')
    pagCustomers = p.get_page(page)
    pageNum = 'd' * pagCustomers.paginator.num_pages

    context = {'users': pagCustomers, 'pagNum': pageNum}
    return render(request, 'account/customers.html', context)


@login_required(login_url='loginPage')
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
        return redirect(request.META.get('HTTP_REFERER'))

    context = {}
    return render(request, 'account/createCustomer.html', context)


@login_required(login_url='loginPage')
@csrf_exempt
def addProduct(request):
    if(request.method == 'POST'):
        productClient = ProductClient()
        name = request.POST.get('name')
        description = request.POST.get('description')
        size = request.POST.get('size')
        dateNow = datetime.datetime.now()
        data = {'name': name, 'description': description,
                'size': size.split(), 'timestamp': dateNow}
        productClient.create(data, name)
        return redirect(request.META.get('HTTP_REFERER'))

    context = {}
    return render(request, 'account/addProduct.html', context)


def updateOrder(request, docId):
    orderClient = OrderClient()
    order = orderClient.get_by_id(docId)
    if(request.method == 'POST'):
        stat = request.POST.get('stat')
        data = {'status': stat}
        orderClient.update(docId, data)
        return redirect(request.META.get('HTTP_REFERER'))
    context = {'order': order}
    return render(request, 'account/updateOrder.html', context)


def deleteOrder(request, docId):
    orderClient = OrderClient()
    order = orderClient.get_by_id(docId)
    userClient = UserClient()
    userData = userClient.get_by_id(order['user_id'])
    userOrdersCount = int(userData['oredersCount'])
    if(request.method == 'POST'):
        orderClient.delete_by_id(docId)
        orderClient.deleteSubCollection(docId)
        userOrdersCount -= 1
        data = {'oredersCount': f'{userOrdersCount}'}
        userClient.update(order['user_id'], data)
        return redirect(request.META.get('HTTP_REFERER'))
    context = {'order': order}
    return render(request, 'account/deleteOrder.html', context)


@csrf_exempt
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Check your username or password')

        context = {}
        return render(request, 'account/login.html', context)


def logoutU(request):
    logout(request)
    return redirect('loginPage')


@login_required(login_url='loginPage')
def orders(request):
    orderClient = OrderClient()
    orders = orderClient.all()
    totalOrders = len(orders)
    p = Paginator(orders, 10)
    page = request.GET.get('page')
    pagOrders = p.get_page(page)

    pageNum = 'd' * pagOrders.paginator.num_pages

    context = {'orders': orders, 'pagOrders': pagOrders,
               'pageNum': pageNum, 'totalOrders': totalOrders}
    return render(request, 'account/orders.html', context)
