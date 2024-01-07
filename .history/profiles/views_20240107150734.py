from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm
from checkout.models import Order

@login_required
def view_profile(request):
    # Retrieve user profile or create a new one if it doesn't exist
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            print("form is valid")
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            print("form errors:", form.errors)
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)

    orders = profile.orders.all()

    template = 'view_profile.html'
    context = {
        'user_profile_form': form,
        'orders': orders,
        'on_profile_page': True,
    }

    return render(request, template, context)

@login_required
def user_orders(request):
    user = request.user
    print("User: ", user)
    user_profile = get_object_or_404(UserProfile, user=user.id)
    print("User profile: ", user_profile)
    all_orders = Order.objects.all()
    print(all_orders)
    # orders = Order.objects.filter(user_profile=user_profile.id)
    orders = user_profile.orders.all()
    print("Orders: ", orders)

    first_order = Order.objects.all()[:1].get()
    print(first_order)

    context = {
        'orders': orders,
    }

    return render(request, 'profiles/user_orders.html', context)