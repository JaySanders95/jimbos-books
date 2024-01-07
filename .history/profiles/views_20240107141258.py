from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm

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

    template = 'profiles/view_profile.html'
    context = {
        'user_profile_form': form,
        'orders': orders,
        'on_profile_page': True,
    }

    return render(request, template, context)

@login_required
def