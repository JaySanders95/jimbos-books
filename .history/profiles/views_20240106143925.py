from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def view_profile(request):
    # Retrieve and display user profile information
    return render(request, 'profiles/view_profile.html', {'user_profile': request.user.profile})