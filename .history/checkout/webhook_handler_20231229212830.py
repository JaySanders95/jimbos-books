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
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=shipping_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.country,
                    postcode__iexact=shipping_details.postal_code,
                    town_or_city__iexact=shipping_details.town_or_city,
                    street_address1__iexact=shipping_details.street_line1,
                    street_address2__iexact=shipping_details.line2,
                    county__iexact=shipping_details.state,
                    grand_total__iexact=shipping_details.grand_total,
                )
            
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt +=1
                time.sleep(1)
        if order_exists:
            self.send_coin
            return HttpResponse(
                content=f'webhook received: {event["type"]} | Success, verified order already in database',
                status=200)
        else:
            order = Order.objects.create(
                full_name=shipping_details.name,
                email=shipping_details.email,
                phone_number=shipping_details.phone,
                country=shipping_details.country,
                postcode=shipping_details.postal_code,
                town_or_city=shipping_details.city,
                street_address1=shipping_details.line1,
                street_address2=shipping_details.line2,
                county=shipping_details.state,
                grand_total=shipping_details.grand_total,
            )

                for item_id, item_data in json.loads(bag).items():
                    try:

                        book = Book.objects.get(id=item_id)
                        order_line_item = OrderLineItem(
                            order=order,
                            book=book,
                            quantity=item_data,
                        )

                        order_line_item.save()
                    except Exception as e:
                        if order:
                            order.delete()
                        return HttpResponse(content=f'webhook received: {event["type"]} | ERROR: {e}', status=500)
                    
        return HttpResponse(
            content=f'webhook received: {event["type"]}',
            status=200)          

    def handle_payment_intent_payment_failed(self, event):

        return HttpResponse(
            content=f'webhook received: {event["type"]}',
            status=200)    
