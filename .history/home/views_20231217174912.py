from django.shortcuts import render
from .models import Book
# Create your views here.

def home(request):
    return render(request, 'home.html')

def book_list(request):
    