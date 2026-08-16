from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from core.views import custom_logout

urlpatterns = [
    path('', views.home_view, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add-product/', views.add_product_view, name='add_product'),
    path('my-ads/', views.my_ads_view, name='my_ads'),
    
    # Edit & Delete Paths
    path('edit-product/<int:product_id>/', views.edit_product_view, name='edit_product'),
    path('delete-product/<int:product_id>/', views.delete_product_view, name='delete_product'),
    
    # AJAX Path for Subcategories (Crucial for add_product form)
    path('ajax/load-subcategories/', views.load_subcategories, name='ajax_load_subcategories'),

    # Login & Logout Paths
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', custom_logout, name='logout'),
    
    path('register/', views.register_view, name='register'),

    path('chat/', views.chat_home_view, name='chat_home'),
    path('chat/<str:username>/', views.chat_room_view, name='chat_room'),

    path('settings/', views.settings_view, name='settings'),
]

# Media Files support for development (DEBUG mode)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)