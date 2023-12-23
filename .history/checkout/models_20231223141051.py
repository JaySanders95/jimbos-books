from django.db import models

# Create your models here.


class Cart(models.Model):
    items = models.ManyToManyField('CartItem', related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_items = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def update_totals(self):
        self.total_items = self.items.count()
        self.total_price = sum(item.book.price * item.quantity for item in self.items.all())
        self.save()

    def __str__(self):
        return f"Cart {self.pk}"

class CartItem(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)