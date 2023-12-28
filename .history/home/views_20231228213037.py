from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.views import View
from django.contrib import messages
from .models import Book, Reviews, Careers
from .forms import ReviewsForm, BookForm, BookUpdateForm, JobForm, ModifyJobForm

"""
View for Home 
"""

def home(request):
    reviews = Reviews.objects.order_by('pk')
    return render(request, 'home.html', {'reviews': reviews})


"""
Views Books/Listing
"""

class BookListView(View):
    template_name = 'books.html'

    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('search_query')

        #I
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

"""
Views for reviews
"""

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


def careers(request):
    live_jobs = Careers.objects.filter(expiry_date__gte=date.today())
    return render(request, 'careers.html', {'live_jobs' : live_jobs})



"""
Views for Staff
"""
def is_staff(user):
    return user.is_staff

@user_passes_test(is_staff)
def staff_settings(request):
    return render(request, 'staff/staff_settings.html')

"""
Views for Staff settings -> Books 
"""

@user_passes_test(is_staff)
def modify_books(request, book_id):
    # Retrieve the book instance using the book_id
    book = get_object_or_404(Book, pk=book_id)

    if request.method == 'POST':
        # If the form is submitted, process the data
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            # Redirect to a success page 
            return render(request, 'staff/book_modified.html')
    else:
        # If it's a GET request, pre-fill the form with the existing book data
        form = BookForm(instance=book)

    return render(request, 'staff/modify_books.html', {'form': form, 'book': book})


@user_passes_test(is_staff)
def view_books(request):
    books = Book.objects.all()
    return render(request, 'staff/view_books.html', {'books': books})

@user_passes_test(is_staff)
def delete_books(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    if request.method == 'POST':
        # This means the deletion is confirmed
        book.delete()
        return render(request, 'staff/book_deleted.html', {'book': book})

    return render(request, 'staff/delete_books.html', {'book': book})

@user_passes_test(is_staff)
def add_book(request):
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
    return render(request, 'staff/book_deleted.html')


# @user_passes_test(is_staff)
# def book_modified(request):
#     return render(request, 'staff/book_modified.html')


"""
Views for Staff settings -> Careers 
"""
@user_passes_test(is_staff)
def add_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Job added successfully")
            return redirect('job_list')
    else:
        form = JobForm()
    
    return render(request, 'staff/add_job.html', {'form' : form})


@user_passes_test(is_staff)
def job_list(request):
    careers = Careers.objects.all()
    return render(request, 'staff/job_list.html', {'careers': careers})


@user_passes_test(is_staff)
def modify_job(request, id):
    job = get_object_or_404(Careers, pk=id)

    if request.method == 'POST':
        form = ModifyJobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_list')

    else:
        form = ModifyJobForm(instance=job)
    
    return render(request, 'staff/modify_job.html', {'job': job, 'form': form})


def delete_job(request, job_id):
    job = get_object_or_404(Careers, pk=job_id)

    if request.method == 'POST'


"""
Views for Staff settings -> Reviews 
"""

@user_passes_test(is_staff)
def view_reviews(request):
    reviews = Reviews.objects.all()
    return render(request, 'staff/view_reviews.html', {'reviews': reviews})


@user_passes_test(is_staff)
def delete_review(request, reviews_id):
    review = get_object_or_404(Reviews, pk=reviews_id)

    if request.method == 'POST':
        # This means the deletion is confirmed
        review.delete()
        return render(request, 'staff/review_deleted.html', {'review': review})

    return render(request, 'staff/delete_review.html', {'review': review})

@user_passes_test(is_staff)
def review_deleted(request):
    return render(request, 'staff/review_deleted.html')