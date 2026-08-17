from django.contrib import admin
from .models import Category, SubCategory, Product, ProductImage, City, UserProfile, ChatMessage

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
    list_display = ('title', 'user', 'price', 'city', 'category', 'subcategory', 'created_at', 'is_approved')
    search_fields = ('title', 'user__username', 'description')
    list_filter = ('city', 'category', 'subcategory', 'created_at', 'is_approved')
    inlines = [ProductImageInline]


# City model registration
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)


# UserProfile model registration
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'whatsapp_number', 'theme_preference')
    search_fields = ('user__username', 'whatsapp_number')


# ChatMessage model registration
@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'product', 'timestamp')
    search_fields = ('sender__username', 'receiver__username', 'message')
    list_filter = ('timestamp',)