from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_bag, name='view_bag')
    path('add/<int:book_id>/', views.add_to_bag, na
]
