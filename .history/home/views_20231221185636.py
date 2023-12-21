from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.views import View
from .models import Book


def home(request):
    return render(request, 'home.html')

class BookListView(view):
    template_name = 'books.html'

    def get(self, request, *args, *kwargs):
        search_query = request.GET.get('search_query')

        if search_query:
            books = Book.objects.filter(
                Q(title__icontains=search_query) |
                Q(a)
            )


# def books(request):
#     template_name = 'books.html'

#     books = Book.objects.all()
#     return render(request, 'books.html', {'books': books})

def book_more_info(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'book_more_info.html', {'book' : book})


# def add_to_cart(request, book_id):
#     book = get_object_or_404(Book, pk=book_id)
#     customer = request.user.customer
#     cart = customer.cart

#     if request.method == 'POST':
#         form = AddToCartForm(request.POST)
#         if form.is_valid():
#             quantity = form.cleaned_data['quantity']

#             # Check if the book is already in the cart
#             cart_item, created = CartItem.objects.get_or_create(book=book, quantity=quantity)

#             # Add the cart item to the customer's cart
#             cart.items.add(cart_item)

#             # Update cart totals
#             cart.update_totals()

#             return render(request, 'cart/success.html', {'book': book, 'quantity': quantity})
#     else:
#         form = AddToCartForm()

#     return render(request, 'cart.html', {'form': form, 'book': book})

# def view_cart(request):
#     customer = request.user.customer
#     cart = customer.cart

#     return render(request, 'cart/view_cart.html', {'cart': cart})