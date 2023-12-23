from django.contrib import admin
from .models import Order, OrderLineItem


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('order_number', 'date', 'delivery_cost', 'order_total', 'grand_total')
    
    fields = ('order_number', 'user_profile', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'delivery_cost',
              'order_total', 'grand_total', 'original_bag',
              'stripe_pid')
    
    
