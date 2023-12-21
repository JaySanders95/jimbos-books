from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from home.models import  

def bag_contents(request):

    bag_items = []
    total = 0 
    product_count = 0
    bag = request.session.get('bag' {})

    for item, quantity in bag.items():
        book = get_object_or_404(Book, pk=item_id)
        total += quantity * book.price
        book_count += quantity
        bag_items.append({
            'item_id': item_id,
            'quantity' : quantity,

        })


    delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE)

    grand_total = delivery + total

    context = {
        'bag_items' : bag_items,
        'total' : total,
        'product_count' : product_count,
        'delivery' : delivery,
        'grand_total' : grand_total
    }

    return context