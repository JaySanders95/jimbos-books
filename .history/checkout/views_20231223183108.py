from django.shortcuts import render

# Create your views here.


def checkout(request):
    bag = request.session.get('bag' {})

    if not bag:
        messages.error(request, "Theres nothing in your bag")
        return redirect(reverse('books'))