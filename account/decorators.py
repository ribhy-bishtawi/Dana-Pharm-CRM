from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticatedUser(viewFun):
    def wrapperFun(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return viewFun(request, *args, **kwargs)
    return wrapperFun
