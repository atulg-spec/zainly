from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.html import format_html  # Import format_html

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name','is_active','is_staff')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Shipping Address', {'fields': ('city','state','pin_code','address')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'phone_number'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    ordering = ('email',)

# Register the CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ('gender',)
    search_fields = ('gender',)

@admin.register(Keywords)
class KeywordsAdmin(admin.ModelAdmin):
    list_display = ('keyword',)
    search_fields = ('keyword',)
    actions = ['bulk_upload_keywords']

    def bulk_upload_keywords(self, request, queryset):
        for keyword in queryset:
            keyword.add_keywords_from_input()
        self.message_user(request, "Bulk upload completed successfully.")
    bulk_upload_keywords.short_description = "Bulk upload keywords from text"

@admin.register(Sizes)
class SizesAdmin(admin.ModelAdmin):
    list_display = ('size',)
    search_fields = ('size',)

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('category', 'short_caption')
    search_fields = ('category', 'short_caption')
    list_filter = ('category',)
    readonly_fields = ('category_image', 'icon')

    def category_image_thumbnail(self, obj):
        if obj.category_image:
            return format_html(f'<img src="{obj.category_image.url}" style="width: 50px; height: 50px;" />')
        return ""
    category_image_thumbnail.short_description = "Category Image"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'status', 'created_at', 'expected_delivery_date')
    search_fields = ('order_id', 'user__username', 'status')
    list_filter = ('status', 'created_at')
    date_hierarchy = 'created_at'
    readonly_fields = ('order_id', 'created_at')
    filter_horizontal = ('products',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'date_time')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    list_filter = ('date_time',)
    readonly_fields = ('date_time',)


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'size', 'quantity', 'ordered')
    list_filter = ('ordered', 'size', 'product', 'user')
    search_fields = ('user__username', 'product__title')
    readonly_fields = ('id',)
    
    # Display related fields in the admin form
    raw_id_fields = ('user', 'product', 'size')
    
    # Ordering by latest first
    ordering = ('-id',)

admin.site.register(Cart, CartAdmin)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of extra forms to display in the inline
    fields = ('image',)
    max_num = 10  # Maximum number of images allowed to be uploaded (optional)
    readonly_fields = ('image_tag',)  # For previewing the image in the admin (optional)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.image.url)
        return ""
    image_tag.short_description = 'Preview'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('category', 'gender')
    inlines = [ProductImageInline]
    readonly_fields = ('created_at', 'updated_at')

    # If you want to display a preview of the main product image in the list display:
    def product_image_tag(self, obj):
        if obj.product_image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.product_image.url)
        return ""
    product_image_tag.short_description = 'Main Image'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')
    search_fields = ('product__title',)

    # Optional: If you want to add an image preview in the ProductImage admin list
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.image.url)
        return ""
    image_tag.short_description = 'Image Preview'
    readonly_fields = ('image_tag',)



admin.site.site_header="Zainly"
admin.site.site_title="Zainly Admin"
# admin.site.index_template="home.html"
admin.site.index_title="Zainly | Admin"

from social_django.models import Nonce,UserSocialAuth,Association
from social_django.admin import Nonce,UserSocialAuth,Association
admin.site.unregister(Nonce)
admin.site.unregister(UserSocialAuth)
admin.site.unregister(Association)

