from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from home.models import Book
from django.shortcuts import redirect
from django.contrib import messages

def remove_item_from_bag(request, item_id):
    # Retrieve the current bag from the session
    bag = request.session.get('bag', {})

    if item_id in bag:
        # Retrieve the book associated with the item_id
        book = get_object_or_404(Book, pk=item_id)
        # Remove the item from the bag
        bag.pop(item_id)
        # Update the bag in the session
        request.session['bag'] = bag
        # Display a removal message
        messages.warning(request, f'{book.title}(s) removed from your bag.')

    # Redirect to the view_bag page
    return redirect('view_bag')


def bag_contents(request):
    # Initialize variables to store bag contents and totals
    bag_items = []
    total = 0
    book_count = 0
    # Retrieve the current bag from the session
    bag = request.session.get('bag', {})

    # Iterate through items in the bag
    for item_id, quantity in bag.items():
        # Retrieve the book associated with the item_id
        book = get_object_or_404(Book, pk=item_id)
        # Calculate the total cost for the current book
        single_total = quantity * book.price
        # Update the overall total and book count
        total += single_total
        book_count += quantity
        # Add item details to the bag_items list
        bag_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'book': book,
            'total': single_total
        })

    # Set delivery cost based on whether there are items in the bag
    if bag_items:
        delivery = int(4)
    else:
        delivery = 0

    # Calculate the grand total
    grand_total = delivery + total

    # Create a context dictionary with bag information
    context = {
        'bag_items': bag_items,
        'total': total,
        'book_count': book_count,
        'delivery': delivery,
        'grand_total': grand_total,
        'remove_item_from_bag': remove_item_from_bag,
    }

    # Return the context dictionary
    return context