from django.contrib import admin
from django.urls import path
from . import views
from .views import book

urlpatterns = [
    path('', views.home, name='home'),
    path('books/<int:book_id>/', book, name='book')
    
]
