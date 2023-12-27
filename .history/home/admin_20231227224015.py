from django.contrib import admin
from .models import Customer, Author, Genre, Book, Reviews, Careers, Job_Type
# Register your models here.

admin.site.register(Customer)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(Reviews)
admin.site.register(Careers)
admin.site.register(Job_Type)