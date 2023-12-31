from decimal import Decimal
from django.conf import settings

def bag_contents(request):

    bag_items = []
    total = 0 
    product_count = 0
    bag = request.session.get('bag' {})

    for item, quantity in bag.items()

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