from django.urls import path
from . import views
from django.conf.urls.static import static


urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('checkout_success/<order_number>', views.checkout_success, name='checkout_success'),
    path('wh/')
    
]