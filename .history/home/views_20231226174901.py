from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.views import View
from django.contrib import messages
from .models import Book, Reviews
from .forms import ReviewsForm



def home(request):
    reviews = Reviews.objects.order_by('pk')
    return render(request, 'home.html', {'reviews': reviews})

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
    



def book_more_info(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'book_more_info.html', {'book' : book})


def create_review(request):
    if request.method == 'POST':
        form = ReviewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your review has been sent.')
            return redirect('home')

    else:
        form = ReviewsForm()

    return render(request, 'create_review.html', {'form': form})

def is_staff(user):
    return user.is_staff

def staff_settings()


@user_passes_test(is_staff)
def modify_books(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return render(request, 'book_modified.html', {'book' : book})
    else:
        form = BookForm(instance=book)
    
    return render(request, 'modify_books.html', {'form' : form, 'book': book})


@user_passes_test(is_staff)
def view_books(request):
    books = Book.objects.all()
    return render(request, 'view_books.html', {'books': books})


@user_passes_test(is_staff)
def delete_books(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    if request.method == 'POST':
        book.delete()
        return render(request, 'book_deleted.html', {'book': book})

    return render(request, 'delete_books.html', {'book': book})


@user_passes_test(is_staff)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'book_added.html', {'form': form})
    else:
        form = BookForm()

    return render(request, 'add_book.html', {'form': form})

        
    