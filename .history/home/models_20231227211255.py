from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django_countries.fields import CountryField
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

# class Cart(models.Model):
#     items = models.ManyToManyField('CartItem', related_name='carts')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     total_items = models.PositiveIntegerField(default=0)
#     total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

#     def update_totals(self):
#         # Update total_items and total_price based on the items in the cart
#         self.total_items = self.items.count()
#         self.total_price = sum(item.book.price * item.quantity for item in self.items.all())
#         self.save()

#     def __str__(self):
#         return f"Cart {self.pk}"

# class CartItem(models.Model):
#     book = models.ForeignKey('Book', on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    country = models.CharField(max_length=100)

class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    country_of_birth = CountryField(default="US")
    about = models.CharField(max_length=400, null=True, blank=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    publication_date = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='books/')
    synopsis = models.CharField(max_length=500, null=True, blank=True)
    stock_available = models.PositiveIntegerField(default=99)
    sku = models.CharField(max_length=254, null=True, blank=True) 

    def __str__(self):
        return self.title

class Reviews(models.Model):
    full_name = models.CharField(max_length=30, null=False, blank=False)
    review_title = models.CharField(max_length=50, null=False, blank=False)
    review_body = models.CharField(max_length=500, null=False, blank=False)
    review_image = models.ImageField(upload_to='book_more_info/', null=True, blank=True)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0, null=False, blank=False)
    date_of_review = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "reviews"

    def __str__(self):
        return self.review_title


class Career(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False),
    description = models.CharField(max_length=200, null=False, blank=False),
    expiry_date = models.DateField()

    def __str__(self):
        return self.title
