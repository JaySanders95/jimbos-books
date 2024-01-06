from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from .models import UserProfile
from .forms import UserProfileForm

@login_required
def view_profile(request):
    # Retrieve user profile or create a new one if it doesn't exist
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True
    }

    form = UserProfileForm(instance=user_profile)
    order = user_profile.orders.all()

    context = {'user_profile': user_profile, 'orders' : orders,}
    return render(request, 'profiles/view_profile.html', context)