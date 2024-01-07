from django.contrib import admin
from django.urls import path
from . import views
from .views import view_profile, user_orders

urlpatterns = [
    path('', views.view_profile, name='view_profile'),
    path('profiles/user_orders/', user_orders, name="")
]