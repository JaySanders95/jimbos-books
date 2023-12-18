from django.shortcuts import render
from .models import Book, CartItem
# Create your views here.

def home(request):
    return render(request, 'home.html')

def books(request):
    books = Book.objects.all()
    return render(request, 'books.html', {'books': books})


def add_to_cart(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    customer = request.user.customer

    # Check if the book is already in the cart
    cart_item, created = CartItem.objects.get_or_create(book=book, quantity=1)

    # Add the cart item to the customer's cart
    customer.cart.add(cart_item)

    return render(request, 'cart/success.html', {'book': book})