from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import UserProfile

@login_required
def view_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    context = {'user_profile': user_profile}
    return render(request, 'profiles/view_profile.html', context)