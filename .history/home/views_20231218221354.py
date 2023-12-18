from django.shortcuts import render
from .models import Book


def books(request):
    books = Book.objects.all()
    return render(request, 'home.html', {'books': books})


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