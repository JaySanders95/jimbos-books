from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.conf import settings

from .forms import OrderForm
from bag.contexts import bag_contents
from home.models import Book
from .models import OrderLineItem, Order

import stripe

# Create your views here.

@require_POST
def cache_checkout_data(request):
    pid = request.POST.get('client_secret').split('_secret')[0]


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'country': request.POST['country'],
            'phone_number': request.POST['phone_number'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }


        order_form = OrderForm(form_data)
        #Form validation
        if order_form.is_valid():
            order = order_form.save()
            for item_id, item_data in bag.items():
                try:
                    book = Book.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        book=book,
                        quantity=item_data,
                    )
                    
                    order_line_item.save()
                    
                
                except Book.DoesNotExist:
                    messages.error(request, "Invalid item in bag.")
                    order.delete()
                    return redirect(reverse('bag'))

            return redirect(reverse('checkout_success', args=[order.order_number]))

        else:
            messages.error(request, 'There was an error with your form')

    else:
        bag = request.session.get('bag', {})

    if not bag:
        messages.error(request, "There's nothing in your bag")
        return redirect(reverse('books'))

    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    #print(intent)

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)

def checkout_success(request, order_number):

    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, "Success")
    
    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order' : order
    }

    return render(request, template, context)