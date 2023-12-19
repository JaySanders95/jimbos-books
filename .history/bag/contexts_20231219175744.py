from decimal import Decimal
from django.conf

def bag_contents(request):

    bag_items = []
    total = 0 
    product_count = 0

    delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE)

    context = {}

    return context