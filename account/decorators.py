from tokenize import group
from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticatedUser(viewFun):
    def wrapperFun(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return viewFun(request, *args, **kwargs)
    return wrapperFun


def allowedUsers(viewFun):
    def wrapper_fun(request, *args, **kwargs):
        group = None
        if(request.user.groups.exists()):
            group = request.user.groups.all()[0].name
        if group == 'admin':
            return viewFun(request, *args, **kwargs)
        else:
            return redirect('orders')
    return wrapper_fun
