from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.db import models

class SiteSettings(models.Model):
    FONT_CHOICES = [
        ('font-sans', 'Sans-serif'),
        ('font-serif', 'Serif'),
        ('font-mono', 'Monospace'),
    ]

    slider1_image = models.ImageField(upload_to='slider_images/', blank=True, null=True)
    slider1_caption1 = models.CharField(max_length=30, blank=True)
    slider1_caption2 = models.CharField(max_length=30, blank=True)
    slider1_url = models.URLField(blank=True)

    slider2_image = models.ImageField(upload_to='slider_images/', blank=True, null=True)
    slider2_caption1 = models.CharField(max_length=30, blank=True)
    slider2_caption2 = models.CharField(max_length=30, blank=True)
    slider2_url = models.URLField(blank=True)

    slider3_image = models.ImageField(upload_to='slider_images/', blank=True, null=True)
    slider3_caption1 = models.CharField(max_length=30, blank=True)
    slider3_caption2 = models.CharField(max_length=30, blank=True)
    slider3_url = models.URLField(blank=True)

    site_name = models.CharField(max_length=15, blank=True)
    site_header_news = CKEditor5Field('Text', config_name='extends')

    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    mobile_logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    slider_background_color = models.CharField(max_length=7, blank=True, help_text="Enter color in HEX format, e.g., #FFFFFF")
    tagline = models.CharField(max_length=100, blank=True)

    main_page_video_thumbnail = models.ImageField(upload_to='slider_images/', blank=True, null=True)
    main_page_video_caption = models.CharField(max_length=30, blank=True)
    main_page_video_url = models.CharField(max_length=300, blank=True)

    instagram = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=150, blank=True)

    instagram_page = models.URLField(blank=True)
    facebook_handle = models.URLField(blank=True)
    twitter_handle = models.URLField(blank=True)
    youtube_handle = models.URLField(blank=True)
    
    font_style = models.CharField(max_length=10, choices=FONT_CHOICES, default='font-sans')

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"


class PaymentGateway(models.Model):
    razorpay_key_id = models.CharField(max_length=500,default="")
    razorpay_key_secret = models.CharField(max_length=500,default="")

    class Meta:
        verbose_name = "Payment Gateway Setting"
        verbose_name_plural = "Payment Gateway"
    def __str__(self):
      return "Payment Gateway"
    

class ProductByCategory(models.Model):
    image = models.ImageField(upload_to='slider_images/', blank=True, null=True)
    url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Product By Category"
        verbose_name_plural = "Product By Category"

    def __str__(self):
        return "Product By Category"