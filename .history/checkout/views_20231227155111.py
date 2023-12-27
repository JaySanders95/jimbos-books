from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm
from bag.contexts 

# Create your views here.


def checkout(request):
    bag = request.session.get('bag', {})

    if not bag:
        messages.error(request, "Theres nothing in your bag")
        return redirect(reverse('books'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form' : order_form,
        'stripe_public_key' : 'pk_test_51OQt1OCH1J0xveRXDKECKstnNxkUbtgbLLAiJqyz3trA3pq5hoV0kvIj51vNjnxa2v1VFeQ8sCzyy7z0fJ1yhjYZ00tp4E1gsb',
        'client_secret' : 'test client secret'

    }

    return render(request, template, context)