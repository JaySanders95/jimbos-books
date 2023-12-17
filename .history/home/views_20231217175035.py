from django.shortcuts import render
from .models import Book
# Create your views here.

def home(request):
    return render(request, 'home.html')

def books_page(request):
    books = Book.objects.all()
    return render(request, 'books.html', {'books': books})