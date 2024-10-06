from PIL import Image
from django.core.files.storage import default_storage
from django.db import models
from django.contrib.auth.models import AbstractUser
from dashboard.manager import *
from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.db.models import UniqueConstraint
import random
from django_ckeditor_5.fields import CKEditor5Field
import string
from django.utils.text import slugify
from cities_light.models import City, Region  # Import city and region models

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone_number = models.PositiveIntegerField(blank=True, null=True)
    pin_code = models.CharField(max_length=50, default="")
    state = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, default="")
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Gender(models.Model):
    gender = models.CharField(max_length=100, default='')
    def __str__(self):
        return f"{self.gender}"
    
    class Meta:
        verbose_name = "Gender"
        verbose_name_plural = "Gender Category"

class Keywords(models.Model):
    keyword = models.CharField(max_length=50, unique=True, default='',null=True,blank=True)
    bulk_upload = models.TextField(default='', null=True, blank=True)

    def __str__(self):
        return f"{self.keyword}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.bulk_upload:
            self.add_keywords_from_input()

    def add_keywords_from_input(self):
        try:
            with transaction.atomic():
                for line in self.bulk_upload.splitlines():
                    word = line.strip()
                    if word:
                        Keywords.objects.get_or_create(keyword=word)
        except Exception as e:
            raise ValidationError(f"Error saving Keywords from input: {e}")

    class Meta:
        verbose_name = "Keyword"
        verbose_name_plural = "Keywords"
        unique_together = ['keyword']

class Sizes(models.Model):
    size = models.CharField(max_length=100, default='')
    def __str__(self):
        return f"{self.size}"
    
    class Meta:
        verbose_name = "Size"
        verbose_name_plural = "Sizes Available"

class Categories(models.Model):
    icon = models.FileField(upload_to='category_images/',null=True,blank=True)
    category_image = models.ImageField(upload_to='category_images/')
    category = models.CharField(max_length=100, default='')
    short_caption = models.CharField(max_length=12, default='')

    def __str__(self):
        return f"Category {self.category}"
    
    class Meta:
        verbose_name = "Categories"
        verbose_name_plural = "Category"


class Product(models.Model):
    title = models.CharField(max_length=30)
    product_image = models.ImageField(upload_to='product_images/')
    second_image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    size_chart = models.ImageField(upload_to='size_chart/', null=True, blank=True)
    category = models.ManyToManyField(Categories)
    gender = models.ManyToManyField(Gender)
    description = CKEditor5Field('Text', config_name='extends')
    keywords = models.ManyToManyField(Keywords)
    stars = models.PositiveIntegerField(default=5)
    review = models.PositiveIntegerField(default=1200)
    before_discount_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_percent = models.PositiveIntegerField(default=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    video_url = models.URLField(blank=True)
    sizes_available = models.ManyToManyField(Sizes)
    slug = models.SlugField(unique=True, max_length=100, blank=True, null=True)  # Slug field with null/blank for existing products
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Automatically generate slug if not present
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image for {self.product.title}"



class Cart(models.Model):
    id=models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, related_name='cart', on_delete=models.CASCADE)
    size = models.ForeignKey(Sizes, related_name='cart', on_delete=models.CASCADE, null=True,blank=True)
    product = models.ForeignKey(Product, related_name='cart', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product}"
    
    class Meta:
        verbose_name = "Cart Items"
        verbose_name_plural = "Cart"
        unique_together = ('user', 'product')
        constraints = [
            UniqueConstraint(fields=['user', 'product'], name='unique_user_product')
        ]


order_status = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Refunded', 'Refunded'),
        ('Failed', 'Failed'),
    ]

def generate_unique_id():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(10))

class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    order_id = models.CharField(max_length=10, unique=True, default=generate_unique_id, editable=False)
    user = models.ForeignKey(CustomUser, related_name='order', on_delete=models.CASCADE)
    products = models.ManyToManyField(Cart, related_name='order')
    status = models.CharField(max_length=16,choices=order_status,default="Pending")
    expected_delivery_date = models.DateField(null=True,blank=True)

    def __str__(self):
        return f"{self.order_id}"
    
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

class Payment(models.Model):
    order_id = models.CharField(max_length=100, unique=True)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='created')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id


class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)  # Assuming a maximum of 15 characters for a phone number
    query = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.last_name else self.first_name
    class Meta:
        verbose_name = "Contact Us Request"
        verbose_name_plural = "Contact Requests"