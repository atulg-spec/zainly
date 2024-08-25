from django.contrib import admin
from .models import SiteSettings
from django_ckeditor_5.widgets import CKEditor5Widget
from django.forms import ModelForm

# Custom form to use CKEditor5 widget in the admin
class SiteSettingsForm(ModelForm):
    class Meta:
        model = SiteSettings
        fields = '__all__'
        widgets = {
            'site_header_news': CKEditor5Widget(config_name='extends'),
        }

class SiteSettingsAdmin(admin.ModelAdmin):
    form = SiteSettingsForm
    
    list_display = ('site_name', 'slider1_caption1', 'slider1_caption2', 'slider2_caption1', 'slider1_caption2', 'slider3_caption1', 'slider1_caption2', 'slider_background_color')
    
    fieldsets = (
        ('Main Settings', {
            'fields': ('site_name','site_header_news', 'logo', 'mobile_logo', 'tagline', 'slider_background_color')
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

admin.site.register(SiteSettings, SiteSettingsAdmin)
