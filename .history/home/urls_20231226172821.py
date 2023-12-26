from django.contrib import admin
from django.urls import path
from . import views
from .views import BookListView

urlpatterns = [
    path('', views.home, name='home'),
    path('reviews/', views.create_review, name='create_review'), 
    path('books/', BookListView.as_view(), name='books'),
    path('books/<int:book_id>/', views.book_more_info, name='book_more_info')
    path('add_book/', view.add_book, name='add_book'),
    path('modify_books/', view.modify_books, name='modify_books'),
    path('view_books/', view.add_book, name='add_book'),
    path('add_book', view.add_book, name='add_book'),
    
]
