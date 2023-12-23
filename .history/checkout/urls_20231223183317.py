from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('books/', BookListView.as_view(), name='books'),
    path('books/<int:book_id>/', views.bofo')
    
]