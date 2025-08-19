from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Category(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    def __str__(self): return self.name

class Product(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=160)
    description = models.TextField()
    price_pkr = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    attributes = models.JSONField(default=dict, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    @property
    def main_image(self):
        return self.images.order_by('position').first()
    def __str__(self): return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    url = models.URLField()
    alt = models.CharField(max_length=200, blank=True)
    position = models.PositiveIntegerField(default=0)
    class Meta: ordering = ['position','id']

class Review(models.Model):
    STATUS = (('PENDING','Pending'),('APPROVED','Approved'),('REJECTED','Rejected'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    rating = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=120)
    body = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: indexes = [models.Index(fields=['product','status'])]

class Order(models.Model):
    STATUS = (('AWAITING_PAYMENT','Awaiting Payment'),('PAID','Paid'),('PENDING_COD','Pending COD'),('SHIPPED','Shipped'),('CANCELLED','Cancelled'))
    email = models.EmailField()
    name = models.CharField(max_length=160)
    phone = models.CharField(max_length=40)
    line1 = models.CharField(max_length=200)
    line2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=120)
    region = models.CharField(max_length=120)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=2, default='PK')
    status = models.CharField(max_length=20, choices=STATUS, default='PENDING_COD')
    payment_method = models.CharField(max_length=20, default='COD')
    total_pkr = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200)
    price_pkr = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)