from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from home.models import Book


# View to render the bag page
def view_bag(request):
    return render(request, 'bag/bag.html')


# View to add items to the shopping bag
def add_to_bag(request, item_id):
    # Extract quantity and redirect URL from the POST request
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    # Retrieve the current bag from the session
    bag = request.session.get('bag', {})

    # Retrieve the book associated with the given item_id
    book = get_object_or_404(Book, pk=item_id)

    # Check if there is enough stock available
    if book.stock_available is not None and quantity > book.stock_available:
        messages.error(request, 'We don\'t have the stock to fulfill your order!')
        return redirect(redirect_url)

    # Update the bag with the selected quantity for the book
    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

    # Update the bag in the session
    request.session['bag'] = bag

    # Display a success message
    messages.success(request, f'{book.title} added to bag.')

    # Redirect back to the original page
    return redirect(redirect_url)
    