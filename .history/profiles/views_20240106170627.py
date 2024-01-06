from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import UserProfile

@login_required
def view_profile(request):
    # Retrieve user profile or create a new one if it doesn't exist
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    form = UserProfileForm(instance=profile)
    order = profile.orders.all()

    context = {'user_profile': user_profile, }
    return render(request, 'profiles/view_profile.html', context)