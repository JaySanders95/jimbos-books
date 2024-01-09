from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.views import View
from django.contrib import messages
from .models import Book, Reviews, Careers
from .forms import ReviewsForm, BookForm, BookUpdateForm, JobForm, ModifyJobForm
from datetime import date
from checkout.models import Order, OrderLineItem

"""
View for Home
"""


def home(request):
    # Retrieve reviews and render the home page
    reviews = Reviews.objects.order_by('pk')
    return render(request, 'home.html', {'reviews': reviews})


"""
Views Books/Listing
"""


class BookListView(View):
    # Class-based view for listing books
    template_name = 'books.html'

    def get(self, request, *args, **kwargs):
        # Retrieve search query from the request
        search_query = request.GET.get('search_query')

        # Returns search by filtered name
        if search_query:
            books = Book.objects.filter(
                Q(title__icontains=search_query) |
                Q(author__name__icontains=search_query) |
                Q(genre__name__icontains=search_query)
            )
        else:
            books = Book.objects.all()

        # Render the books page with the filtered or all books
        return render(request, 'books.html', {'books': books})


def book_more_info(request, book_id):
    # View for displaying detailed information about a book
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'book_more_info.html', {'book': book})


"""
Views for reviews
"""


def create_review(request):
    '''
    View for creating a review, handles form validation and sends a message
    '''
    if request.method == 'POST':
        form = ReviewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your review has been sent.')
            return redirect('home')

    else:
        form = ReviewsForm()

    return render(request, 'create_review.html', {'form': form})


def careers_view(request):
    # View for displaying available careers
    careers = Careers.objects.all()
    context = {'careers': careers}
    return render(request, 'careers.html', context)


"""
Views for Staff
"""


def is_staff(user):
    return user.is_staff


@user_passes_test(is_staff)
def all_orders(request):
    # View for displaying all orders (accessible by staff only)
    orders = Order.objects.all()
    return render(request, 'staff/all_orders.html', {'orders': orders})


@user_passes_test(is_staff)
def staff_settings(request):
    # View for staff settings
    return render(request, 'staff/staff_settings.html')


"""
Views for Staff settings -> Books
"""


@user_passes_test(is_staff)
def modify_books(request, book_id):
    # View for modifying book details (accessible by staff only)
    book = get_object_or_404(Book, pk=book_id)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return render(request, 'staff/book_modified.html')
    else:
        form = BookForm(instance=book)

    return render(request, 'staff/modify_books.html', {'form': form, 'book': book})


@user_passes_test(is_staff)
def view_books(request):
    # View for displaying all books (accessible by staff only)
    books = Book.objects.all()
    return render(request, 'staff/view_books.html', {'books': books})


@user_passes_test(is_staff)
def delete_books(request, book_id):
    # View for deleting a book (accessible by staff only)
    book = get_object_or_404(Book, pk=book_id)

    if request.method == 'POST':
        book.delete()
        return render(request, 'staff/book_deleted.html', {'book': book})

    return render(request, 'staff/delete_books.html', {'book': book})


@user_passes_test(is_staff)
def add_book(request):
    # View for adding a new book (accessible by staff only)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'staff/book_added.html', {'form': form})
    else:
        form = BookForm()

    return render(request, 'staff/add_book.html', {'form': form})


@user_passes_test(is_staff)
def book_deleted(request):
    # View for displaying a message after deleting a book (accessible by staff only)
    return render(request, 'staff/book_deleted.html')


"""
Views for Staff settings -> Careers
"""


@user_passes_test(is_staff)
def add_job(request):
    # View for adding a new job (accessible by staff only)
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Job added successfully")
            return redirect('job_list')
    else:
        form = JobForm()

    return render(request, 'staff/add_job.html', {'form': form})


@user_passes_test(is_staff)
def job_list(request):
    # View for displaying the list of available jobs (accessible by staff only)
    careers = Careers.objects.all()
    return render(request, 'staff/job_list.html', {'careers': careers})


@user_passes_test(is_staff)
def modify_job(request, id):
    # View for modifying job details (accessible by staff only)
    job = get_object_or_404(Careers, pk=id)

    if request.method == 'POST':
        form = ModifyJobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_list')

    else:
        form = ModifyJobForm(instance=job)

    return render(request, 'staff/modify_job.html', {'job': job, 'form': form})


def delete_job(request, id):
    # View for deleting a job (accessible by staff only)
    job = get_object_or_404(Careers, pk=id)

    if request.method == 'POST':
        job.delete()
        messages.success(request, "Job deleted successfully")
        return redirect('job_list')

    return render(request, 'staff/delete_job.html', {'job': job})


"""
Views for Staff settings -> Reviews
"""


@user_passes_test(is_staff)
def view_reviews(request):
    # View for displaying all reviews (accessible by staff only)
    reviews = Reviews.objects.all()
    context = {'reviews': reviews}
    return render(request, 'view_reviews.html', context)


@user_passes_test(is_staff)
def delete_review(request, review_id):
    # View for deleting a review (accessible by staff only)
    review = Reviews.objects.get(id=review_id)
    review.delete()
    return redirect('view_reviews')


@user_passes_test(is_staff)
def review_deleted(request):
    # View for displaying a message after deleting a review (accessible by staff only)
    return render(request, 'staff/review_deleted.html')
