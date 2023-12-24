from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.views import View
from .models import Book


def home(request):
    return render(request, 'home.html')

class BookListView(View):
    template_name = 'books.html'

    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('search_query')

        if search_query:
            books = Book.objects.filter(
                Q(title__icontains=search_query) |
                Q(author__name__icontains=search_query) |
                Q(genre__name__icontains=search_query)
            )
        else:
            books = Book.objects.all()

        return render(request, 'books.html', {'books': books})
    


# def books(request):
#     template_name = 'books.html'

#     books = Book.objects.all()
#     return render(request, 'books.html', {'books': books})

def book_more_info(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'book_more_info.html', {'book' : book})


Class ReviewsForm()
    