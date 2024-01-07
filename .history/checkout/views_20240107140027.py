from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.conf import settings

from .forms import OrderForm
from bag.contexts import bag_contents
from home.models import Book
from profiles.models import UserProfile
from .models import OrderLineItem, Order
from .models import UserProfile

import stripe
import json

# This code was taken from the boutique ado with my own modifications

@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        print(f"PaymentIntent ID: {pid}")  # Log PaymentIntent ID
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag' : json.dumps(request.session.get('bag', {})),
            'username' : request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        print(f'Error processing cache checkout data: {e}')  # Log error
        message.error(request, 'Sorry, your payment could not be made, please try again.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    user = request.user
    
    if user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            pass

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

        if request.user.is_authenticated:
            # If the user is logged in, save the information to their profile
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            user_profile.full_name = form_data['full_name']
            user_profile.email = form_data['email']
            user_profile.country = form_data['country']
            user_profile.phone_number = form_data['phone_number']
            user_profile.postcode = form_data['postcode']
            user_profile.town_or_city = form_data['town_or_city']
            user_profile.street_address1 = form_data['street_address1']
            user_profile.street_address2 = form_data['street_address2']
            user_profile.county = form_data['county']
            user_profile.save()
        #Form validation
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()
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

        if user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=user)
                initial_data = {
                    'full_name': user_profile.full_name,
                    'email': user_profile.email,
                    'country': user_profile.country,
                    'phone_number': user_profile.phone_number,
                    'postcode': user_profile.postcode,
                    'town_or_city': user_profile.town_or_city,
                    'street_address1': user_profile.street_address1,
                    'street_address2': user_profile.street_address2,
                    'county': user_profile.county,
                }
            except UserProfile.DoesNotExist:
                pass

        order_form = OrderForm(initial=initial_data)

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