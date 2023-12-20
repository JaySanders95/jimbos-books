from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.books)
    path('<int:book_id>/', views.book, name='book')
    
]
