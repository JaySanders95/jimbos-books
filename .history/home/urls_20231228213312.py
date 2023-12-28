from django.contrib import admin
from django.urls import path
from . import views
from .views import BookListView

urlpatterns = [
    path('', views.home, name='home'),
    path('reviews/', views.create_review, name='create_review'), 
    path('books/', BookListView.as_view(), name='books'),
    path('books/<int:book_id>/', views.book_more_info, name='book_more_info'),
    path('staff/', views.staff_settings, name='staff_settings'),

    
    path('staff/add_book/', views.add_book, name='add_book'),
    path('staff/modify_books/<int:book_id>/', views.modify_books, name='modify_books'),
    path('staff/delete_books/<int:book_id>/', views.delete_books, name='delete_books'),
    path('staff/view_books/', views.view_books, name='view_books'),
    
    path('staff/view_reviews/', views.view_reviews, name='view_reviews'),
    
    path('staff/delete_review/<int:reviews_id>/', views.delete_review, name='delete_review'),

    #Staff/careers
    path('staff/add_job/', views.add_job, name='add_job'),
    path('staff/job_list/', views.job_list, name='job_list'),
    path('staff/modify_job/<int:id>/', views.modify_job, name='modify_job'),
    path('staff/delete_job/<int:id>/', views.delete_job, name='delete_job'),

    #Careers/
    path('careers/', views.careers, name='careers'),


    
]
