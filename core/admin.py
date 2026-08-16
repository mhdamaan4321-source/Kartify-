from django.contrib import admin
from .models import Product, ProductImage
from django.contrib import admin
from .models import Product, City, Category, ProductImage

# Product Image-ah product page-laye display panna Inline
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

# Product model display and management
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'price', 'city', 'category')
    search_fields = ('title', 'user__username')
    list_filter = ('city', 'category')
    inlines = [ProductImageInline]

# Category model registration (Admin only)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

# City model registration (Admin only)
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)