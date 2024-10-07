from django.contrib import admin
from .models import *
from django_ckeditor_5.widgets import CKEditor5Widget
from django.forms import ModelForm
from django.utils.html import format_html

# Custom form to use CKEditor5 widget in the admin
class SiteSettingsForm(ModelForm):
    class Meta:
        model = SiteSettings
        fields = '__all__'
        widgets = {
            'site_header_news': CKEditor5Widget(config_name='extends'),
        }

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    form = SiteSettingsForm

    list_display = ('site_name', 'slider1_image_tag', 'slider2_image_tag', 'slider3_image_tag', 'logo_tag', 'mobile_logo_tag', 'slider_background_color')

    fieldsets = (
        ('Main Settings', {
            'fields': ('site_name', 'site_header_news', 'logo', 'mobile_logo', 'tagline', 'slider_background_color', 'font_style')
        }),
        ('Slider 1', {
            'fields': ('slider1_image', 'slider1_caption1', 'slider1_caption2', 'slider1_url')
        }),
        ('Slider 2', {
            'fields': ('slider2_image', 'slider2_caption1', 'slider2_caption2', 'slider2_url')
        }),
        ('Slider 3', {
            'fields': ('slider3_image', 'slider3_caption1', 'slider3_caption2', 'slider3_url')
        }),
        ('Index Page Video', {
            'fields': ('main_page_video_thumbnail', 'main_page_video_caption', 'main_page_video_url')
        }),
        ('Index Page Timer', {
            'fields': ('main_page_timer_thumbnail', 'main_page_timer_caption', 'discount_percentage','last_price','current_price','main_page_timer','main_page_timer_url')
        }),
        ('Contact Info', {
            'fields': ('instagram', 'phone_number', 'email', 'location')
        }),
        ('Social Media', {
            'fields': ('instagram_page', 'facebook_handle', 'twitter_handle', 'youtube_handle')
        }),
    )

    def has_add_permission(self, request):
        # Allows addition only if no instance exists
        return not SiteSettings.objects.exists()

    # Display images in the admin panel
    def slider1_image_tag(self, obj):
        if obj.slider1_image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.slider1_image.url)
        return "No Image"

    def slider2_image_tag(self, obj):
        if obj.slider2_image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.slider2_image.url)
        return "No Image"

    def slider3_image_tag(self, obj):
        if obj.slider3_image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.slider3_image.url)
        return "No Image"

    def logo_tag(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.logo.url)
        return "No Logo"

    def mobile_logo_tag(self, obj):
        if obj.mobile_logo:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.mobile_logo.url)
        return "No Mobile Logo"

    # Short descriptions for each image tag
    slider1_image_tag.short_description = 'Slider 1 Image'
    slider2_image_tag.short_description = 'Slider 2 Image'
    slider3_image_tag.short_description = 'Slider 3 Image'
    logo_tag.short_description = 'Logo'
    mobile_logo_tag.short_description = 'Mobile Logo'



class PaymentGatewayAdmin(admin.ModelAdmin):
    list_display = ('razorpay_key_id', 'razorpay_key_secret')
    search_fields = ('razorpay_key_id',)

    def has_add_permission(self, request):
        # Restrict adding more than one PaymentGateway object
        if PaymentGateway.objects.exists():
            return False
        return super().has_add_permission(request)

admin.site.register(PaymentGateway, PaymentGatewayAdmin)

class ProductByCategoryAdmin(admin.ModelAdmin):
    list_display = ('display_image', 'url')  # Include the display_image method
    search_fields = ('url',)
    list_filter = ('image',)
    ordering = ('url',)

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Image'  # Column header name in the admin

# Register the model with the admin interface
admin.site.register(ProductByCategory, ProductByCategoryAdmin)
