from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from home.models import Book

# Create your views here.

def view_bag(request):
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    book = get_object_or_404(Book, pk=item_id)
    if book.stock.available is not None and quantity > book.stock_available:
        messages.error(request, 'We dont have the stock to fulfill your order!')
        return redirect(redirect_url)


    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

    request.session['bag'] = bag

    messages.success(request, 'Item added to your bag!')

    return redirect(redirect_url)

