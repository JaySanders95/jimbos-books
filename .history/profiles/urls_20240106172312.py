from django.urls import path
from .views import view_profile

urlpatterns = [
    path('', views.view_profile, name='view_profile'),
]