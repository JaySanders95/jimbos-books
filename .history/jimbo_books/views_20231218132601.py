from django.shortcuts import render, redirect
from cart.cart import Cart
from .models import Book

def cart_remove(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        book = Book.objects.get(id=book_id)

        cart = Cart(request)
        cart.remove(book)

        return redirect('cart_detail')
    return redirect('cart_detail')

