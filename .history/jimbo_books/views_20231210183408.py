from django.shortcuts import render

def home(request):
    return render(request, 'jimbo_books/home.html')