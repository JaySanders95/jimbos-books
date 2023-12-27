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

    if request.method == 'POST':
        bag = request.session.get('bag', {})

    
    else:
        bag = request.session.get('bag', {})

        form_data = {
            'full_name' : request.POST['full_name'],
            'email' : request.POST['email'],
            'phone_number' : request.POST['phone_number'],
            'country' : request.POST['country'],
            'postcode' : request.POST['postcode'],
            'town_or_city' : request.POST['town_or_city'],
            'street_address1' : request.POST['street_address1'],
            'street_address2' : request.POST['street_address2'],
            'county' : request.POST['county'],
        }

        order_form = OrderForm(form_data)

        if order_form.is_valid():
            order_form.save()

            for item_id, item_data in bag.items():
                try:
                    book = Book.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        book=book,
                        quantity=item_data,
                    )
                    order_line_item.save()
                
                except: Book.DoesNotExist:
                    messages.error(request, "invalid item in bag.")
                    order.delete()
                    return redirect()
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
        'stripe_public_key' : stripe_public_key,
        'client_secret' : intent.client_secret,

    }

    return render(request, template, context)