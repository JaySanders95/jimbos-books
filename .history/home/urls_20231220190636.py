from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/<int:book_id>/', viewsbook, name='book')
    
]
