from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.html import format_html  # Import format_html
from django.urls import reverse
from django.utils.http import urlencode


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
    list_display = ('icon_tag','category_image_tag','category', 'short_caption')
    search_fields = ('category', 'short_caption')

    def icon_tag(self, obj):
        if obj.icon:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.icon.url)
        return ""
    icon_tag.short_description = 'Icon Preview'

    def category_image_tag(self, obj):
        if obj.category_image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.category_image.url)
        return ""
    category_image_tag.short_description = 'Category Image Preview'

    readonly_fields = ('icon_tag', 'category_image_tag')  # Make the image previews read-only

@admin.register(RecentlyStalked)
class RecentlyStalkedAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')  # Adjust fields as necessary
    search_fields = ('user__first_name', 'product__title')  # Enable searching by user first name and product title



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('product_details', 'user','created_at', 'expected_delivery_date', 'status','order_id')
    search_fields = ('order_id', 'user__username', 'status')
    list_filter = ('status', 'created_at')
    date_hierarchy = 'created_at'
    readonly_fields = ('order_id', 'created_at')
    filter_horizontal = ('products',)

    def product_details(self, obj):
        cart_items = obj.products.all()
        product_details_list = []

        for cart_item in cart_items:
            product = cart_item.product
            # Generate public URL using product slug
            product_public_url = reverse('product-view', kwargs={'slug': product.slug})
            
            details = format_html(
                """
                <div style="margin-bottom: 10px;">
                    <img src="{}" style="max-height: 50px;" /><br>
                    <strong>Title:</strong> <a href="{}">{}</a><br>
                    <strong>Price:</strong> ₹{}<br>
                    <strong>Quantity:</strong> {}<br>
                </div>
                """,
                product.product_image.url if product.product_image else '',
                product_public_url,  # Link to public product page
                product.title,
                product.price,
                cart_item.quantity
            )
            product_details_list.append(details)

        return format_html(''.join(product_details_list)) if product_details_list else "No products"

    product_details.short_description = 'Product Details'


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'date_time')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    list_filter = ('date_time',)
    readonly_fields = ('date_time',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'size', 'quantity', 'ordered', 'product_image_tag')
    search_fields = ('user__username', 'product__title')  # Search by username and product title
    list_filter = ('ordered', 'size')
    readonly_fields = ('product_image_tag',)

    def product_image_tag(self, obj):
        if obj.product and obj.product.product_image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.product.product_image.url)
        return ""
    product_image_tag.short_description = 'Product Image'


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


class ProductImageInline(admin.TabularInline):  # Inline to manage product images
    model = ProductImage
    extra = 1  # Number of empty forms to display
    readonly_fields = ('image_tag',)  # Display image preview

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.image.url)
        return ""
    image_tag.short_description = 'Image Preview'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'product_image_tag', 
        'title', 
        'price', 
        'stars', 
        'review', 
        'created_at', 
        'updated_at'
    )
    search_fields = ('title', 'description')
    list_filter = ('category', 'gender', 'stars')  # Added stars to the filters
    inlines = [ProductImageInline]
    readonly_fields = ('created_at', 'updated_at', 'slug')

    # Display a preview of the main product image in the list display
    def product_image_tag(self, obj):
        if obj.product_image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.product_image.url)
        return ""
    product_image_tag.short_description = 'Main Image'

    # Optionally add custom CSS for better appearance
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)  # Link to a custom CSS file if needed
        }

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product_image_tag','image_tag','product')  # Include product image tag for display
    search_fields = ('product__title',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.image.url)
        return ""
    image_tag.short_description = 'Image Preview'

    def product_image_tag(self, obj):
        if obj.product:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.product.product_image.url)
        return ""
    product_image_tag.short_description = 'Product Main Image'

    readonly_fields = ('image_tag',)  # Make image_tag read-only


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'payment_id', 'amount', 'status', 'created_at')
    search_fields = ('order_id', 'payment_id', 'status')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)

admin.site.register(Payment, PaymentAdmin)



admin.site.site_header="The Zainly"
admin.site.site_title="The Zainly Admin"
# admin.site.index_template="home.html"
admin.site.index_title="The Zainly | Admin"

from social_django.models import Nonce,UserSocialAuth,Association
from social_django.admin import Nonce,UserSocialAuth,Association
admin.site.unregister(Nonce)
admin.site.unregister(UserSocialAuth)
admin.site.unregister(Association)

