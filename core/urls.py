from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_view, name='home'),
    path('product/<int:product_id>/', views.product_detail_view, name='product_detail'),
    path('add-product/', views.add_product_view, name='add_product'),
    path('my-ads/', views.my_ads_view, name='my_ads'),
    
    # Edit & Delete Paths (Ithuvaan miss aayirunthathu)
    path('edit-product/<int:product_id>/', views.edit_product_view, name='edit_product'),
    path('delete-product/<int:product_id>/', views.delete_product_view, name='delete_product'),
    
    # Login & Logout Paths
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register_view, name='register'),
]

# Media Files support for development (DEBUG mode)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)