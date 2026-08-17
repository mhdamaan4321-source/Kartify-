from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Home & Authentication URLs
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    
    # Product Management URLs (Updated to match add_product and my_ads function names)
    path('add-product/', views.add_product, name='add_product'),
    path('my-ads/', views.my_ads, name='my_ads'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/edit/<int:product_id>/', views.edit_product_view, name='edit_product'),
    path('product/delete/<int:product_id>/', views.delete_product_view, name='delete_product'),
    
    # Chat Messaging URLs
    path('chat/', views.chat_home_view, name='chat_home'),
    path('chat/<str:username>/', views.chat_room_view, name='chat_room'),

    # AJAX & Settings URLs
    path('ajax/load-subcategories/', views.load_subcategories, name='load_subcategories'),
    path('settings/', views.settings_view, name='settings'),
]

# Media files serving during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)