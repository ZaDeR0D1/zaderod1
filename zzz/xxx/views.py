from django.shortcuts import render, HttpResponse

# Create your views here.


def print_hello(request):
    return HttpResponse(''Hello World'')
