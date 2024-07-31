from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

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

admin.site.register(Slider)
admin.site.register(Gender)
admin.site.register(Categories)
admin.site.register(Cart)
admin.site.register(Order)
@admin.register(Keywords)
class Keywords(admin.ModelAdmin):
    list_display = ('keyword',)
    search_fields = ('keyword',)

@admin.register(Product)
class Product(admin.ModelAdmin):
    list_display = ('title','price','available','created_at','updated_at')
    list_filter = ('category', 'gender','price','available','created_at','updated_at')
    search_fields = ('category', 'gender','price','available','created_at','updated_at','title','description','keywords')

@admin.register(ProductImage)
class ProductImage(admin.ModelAdmin):
    list_display = ('product','uploaded_at')
    list_filter = ('product','uploaded_at')

admin.site.register(Sizes)
# admin.site.register(Cart)


admin.site.site_header="Zainly"
admin.site.site_title="Zainly Admin"
# admin.site.index_template="home.html"
admin.site.index_title="Zainly | Admin"

from social_django.models import Nonce,UserSocialAuth,Association
from social_django.admin import Nonce,UserSocialAuth,Association
admin.site.unregister(Nonce)
admin.site.unregister(UserSocialAuth)
admin.site.unregister(Association)

