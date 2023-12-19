from decimal import Decimal
from django.conf import settings

def bag_contents(request):

    bag_items = []
    total = 0 
    product_count = 0

    delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE)

    grand_total = delivery + total

    context = {
        bag_items
        total
        product_count
    }

    return context