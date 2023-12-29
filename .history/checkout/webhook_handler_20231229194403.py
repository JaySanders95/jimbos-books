from django.http import HttpResponse


class StripeWH_Handler:

    def __init__(self, request):
        self.request = request

        