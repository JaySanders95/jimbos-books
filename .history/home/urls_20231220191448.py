from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.books, name='books'),
    path('books/<pk:book_id>/', views.book_more_info, name='book_more_info')
    
]
