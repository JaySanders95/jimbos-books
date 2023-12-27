from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm
from bag.contexts import bag_contents
from django.conf import settings

import stripe

# Create your views here.


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY



    bag = request.session.get('bag', {})

    if not bag:
        messages.error(request, "Theres nothing in your bag")
        return redirect(reverse('books'))


    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,

    )

    print(intent)

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form' : order_form,
        'stripe_public_key' : 'pk_test_51OQt1OCH1J0xveRXDKECKstnNxkUbtgbLLAiJqyz3trA3pq5hoV0kvIj51vNjnxa2v1VFeQ8sCzyy7z0fJ1yhjYZ00tp4E1gsb',
        'client_secret' : 'test client secret'

    }

    return render(request, template, context)