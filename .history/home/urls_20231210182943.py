urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
]
