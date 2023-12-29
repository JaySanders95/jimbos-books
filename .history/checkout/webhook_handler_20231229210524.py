from django.http import HttpResponse


class StripeWH_Handler:

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):

        return HttpResponse(
            content=f'webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):

        
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info

        # Get the Charge object
        stripe_charge = stripe.Charge.retrieve(
            intent.latest_charge
        )

        billing_details = stripe_charge.billing_details # updated
        shipping_details = intent.shipping
        grand_total = round(stripe_charge.amount / 100, 2) # updated

        for field, value in shipping_details.address.items():
            if value == '':
                shipping_details.address[field] = None

        order_exists = False
        order = Order.objects.get(
            full_name__iexact=shipping_details.name,
            email__iexact=shipping_details.email,
            phone_number__iexact=shipping_details.phone_number,
            country__iexact=shipping_details.country,
            postcode__iexact=shipping_details.postcode,
            town_or_city__iexact=shipping_details.town_or_city,
            street_address1__iexact=shipping_details.name,
            street_address2__iexact=shipping_details.name,
            county__iexact=shipping_details.name,
            grand_total__iexact=shipping_details.name,
        )

        return HttpResponse(
            content=f'webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_payment_failed(self, event):

        return HttpResponse(
            content=f'webhook received: {event["type"]}',
            status=200)    
