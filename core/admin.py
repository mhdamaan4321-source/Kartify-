from django.contrib import admin
from .models import Category, SubCategory, Product, ProductImage, City

# SubCategory-ah Category page-laye add panna Inline
class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryInline]
    list_display = ('name',)

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)


# Product Image-ah product page-laye display panna Inline
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

# Product model display and management
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'price', 'city', 'category', 'subcategory')
    search_fields = ('title', 'user__username')
    list_filter = ('city', 'category', 'subcategory')
    inlines = [ProductImageInline]


# City model registration (Admin only)
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)