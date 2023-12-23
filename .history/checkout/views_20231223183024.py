from django.shortcuts import render

# Create your views here.


def checkout(request):
    bag = request.session.get()