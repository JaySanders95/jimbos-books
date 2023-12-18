from django.shortcuts import render
from .models import Book, CartItem, Cart
from .forms import AddToCartForm

def home(request):
    return render(request, 'home.html')

def books(request):
    books = Book.objects.all()
    return render(request, 'books.html', {'books': books})


~