from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from app.models import Category, Product_Specifications, ProductImage, Products, Specification, User

# Register your models here.


class UserModelAdmin(BaseUserAdmin):
   

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["id","email", "name", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        ("user Credentials", {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email","id"]
    filter_horizontal = []

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('Category_id', 'Category_name')

@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('image',)

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'product_name', 'product_price', 'stock_quantity', 'category', 'created_at', 'updated_at')

@admin.register(Product_Specifications)
class ProductSpecificationsAdmin(admin.ModelAdmin):
    list_display = ('product', 'specification', 'value')
# Now register the new UserAdmin...
admin.site.register(User, UserModelAdmin)
