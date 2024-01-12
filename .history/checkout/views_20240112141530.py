from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.conf import settings
from django.contrib.auth.models import User

from .forms import OrderForm
from bag.contexts import bag_contents
from home.models import Book
from profiles.models import UserProfile
from .models import OrderLineItem, Order
from .models import UserProfile

import stripe
import json

# This code was taken from the boutique ado with my own modifications


# View to cache checkout data for Stripe
@require_POST
def cache_checkout_data(request):
    try:
        # Extract PaymentIntent ID from the request
        pid = request.POST.get('client_secret').split('_secret')[0]
        print(f"PaymentIntent ID: {pid}")  # Log PaymentIntent ID
        stripe.api_key = settings.STRIPE_SECRET_KEY
        # Modify the PaymentIntent metadata with bag and username information
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        print(f'Error processing cache checkout data: {e}')  # Log error
        message.error(request, 'Sorry, your payment could not be made, please try again.')
        return HttpResponse(content=e, status=400)


# View to handle the checkout process
def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    user = request.user

    # Check if the user is authenticated
    if user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            pass
    else:
        bag = request.session.get('bag', {})

    # Handle POST request for form submission
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

        # Create an OrderForm instance with the submitted data
        order_form = OrderForm(form_data)

        # Update user profile information if the user is authenticated
        if request.user.is_authenticated:
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            user_profile.update_profile(form_data)

        # Form validation
        if order_form.is_valid():
            # Save the order and associated order line items
            order = order_form.save_order(request.user, request.session.get('bag', {}))
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form')

    # Handle GET request for rendering the checkout page
    else:
        bag = request.session.get('bag', {})
        initial_data = {}

        # If the user is authenticated, pre-fill the form with user profile data
        if user.is_authenticated:
            initial_data = user.get_profile_data()
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

    # If the bag is empty, display an error message and redirect to books page
    if not bag:
        messages.error(request, "There's nothing in your bag")
        return redirect(reverse('books'))

    # Calculate Stripe total and create a PaymentIntent
    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    # Prepare context for rendering the checkout page
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


# View to render the checkout success page
def checkout_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, "Success")

    # Clear the bag from the session
    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order
    }

    return render(request, template, context)
