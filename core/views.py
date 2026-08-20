from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
import requests
from .models import Product, City, Category, SubCategory, ProductImage, ChatMessage, UserProfile
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm

# Chat Home View
@login_required
def chat_home_view(request):
    chats = ChatMessage.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).distinct().order_by('-timestamp')
    return render(request, 'core/chat_home.html', {'chats': chats})

# Chat Room View
@login_required
def chat_room_view(request, username):
    receiver = get_object_or_404(User, username=username)
    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            ChatMessage.objects.create(sender=request.user, receiver=receiver, message=message_text)
            return redirect('chat_room', username=username)
            
    messages_list = ChatMessage.objects.filter(
        (Q(sender=request.user) & Q(receiver=receiver)) | 
        (Q(sender=receiver) & Q(receiver=request.user))
    ).order_by('timestamp')
    
    return render(request, 'core/chat_room.html', {'receiver': receiver, 'messages_list': messages_list})          

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('home')

# Custom Logout View Alias (Just in case)
def custom_logout(request):
    logout(request)
    return redirect('home')

# AJAX view to load subcategories dynamically based on selected category
def load_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)

# Home Page View
def home(request):
    products = Product.objects.filter(is_approved=True).order_by('-id')
    cities = City.objects.all()
    categories = Category.objects.all()
    
    # Last 1 week-kulla add aanathu (Explore Products / Horizontal Scrolling)
    one_week_ago = timezone.now() - timedelta(days=7)
    recent_products = Product.objects.filter(created_at__gte=one_week_ago, is_approved=True).order_by('-created_at')
    
    query = request.GET.get('q')
    if query:
        products = products.filter(title__icontains=query)
        recent_products = recent_products.filter(title__icontains=query)
        
    city_id = request.GET.get('city')
    if city_id:
        products = products.filter(city_id=city_id)
        recent_products = recent_products.filter(city_id=city_id)
        
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
        recent_products = recent_products.filter(category_id=category_id)
        
    context = {
        'products': products,
        'recent_products': recent_products,
        'cities': cities,
        'categories': categories,
        'search_query': query if query else '',
        'selected_city': city_id if city_id else '',
        'selected_category': category_id if category_id else '',
    }
    return render(request, 'core/home.html', context)

# Product Detail View
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    similar_products = Product.objects.filter(category=product.category, is_approved=True).exclude(pk=product.pk)[:4]
    
    context = {
        'product': product,
        'similar_products': similar_products,
    }
    return render(request, 'core/product_detail.html', context)

# Add to Cart View
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Neenga Cart model create panniruntha anga save pannanum.
    # Eg: Cart.objects.get_or_create(user=request.user, product=product)
    messages.success(request, f"{product.title} added to cart successfully!")
    return redirect(request.META.get('HTTP_REFERER', 'home'))

# User Registration View
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})

# My Ads View
@login_required
def my_ads(request):
    products = Product.objects.filter(user=request.user).order_by('-id')
    return render(request, 'core/my_ads.html', {'products': products})

# Helper function to send WhatsApp notification
def send_whatsapp_alert(message_body):
    import urllib.parse
    recipients = ["+94751205296", "+94766961883"]
    apikey = "YOUR_API_KEY"
    encoded_message = urllib.parse.quote(message_body)
    for phone in recipients:
        url = f"https://api.callmebot.com/whatsapp.php?phone={phone}&text={encoded_message}&apikey={apikey}"
        try:
            requests.get(url)
        except Exception as e:
            print(f"WhatsApp notification error for {phone}:", e)

# Add Product View
@login_required
def add_product(request):
    if request.method == 'POST':
        title = request.POST.get('name', '')
        description = request.POST.get('description', '')
        
        FORBIDDEN_WORDS = ['adult', 'sex', 'nude', 'porn', 'xxx', 'explicit', 'badword1']
        content_to_check = (title + " " + description).lower()
        is_inappropriate = any(word in content_to_check for word in FORBIDDEN_WORDS)
        
        if is_inappropriate:
            messages.error(request, "⚠️ SECURITY ALERT! Inappropriate/Sexual content detected. Product blocked & Alarm triggered for Admin/Staff!")
            request.session['trigger_alarm'] = True
            return redirect('add_product')
        
        if 'trigger_alarm' in request.session:
            del request.session['trigger_alarm']

        product = Product.objects.create(
            user=request.user,
            title=title,
            price=request.POST.get('price'),
            description=description,
            phone_number=request.POST.get('phone_number'),
            city_id=request.POST.get('city'),
            category_id=request.POST.get('category'),
            subcategory_id=request.POST.get('subcategory') if request.POST.get('subcategory') else None,
            is_approved=True
        )
        
        images = request.FILES.getlist('images')
        for img in images:
            ProductImage.objects.create(product=product, image=img)
            
        whatsapp_message = f"📢 New Product Added!\nTitle: {product.title}\nPrice: LKR {product.price}\nSeller: {request.user.username}"
        send_whatsapp_alert(whatsapp_message)
        
        messages.success(request, "Product added successfully! WhatsApp notification sent to Admin & Staff.")
        return redirect('home')
    
    cities = City.objects.all()
    categories = Category.objects.all()
    return render(request, 'core/add_product.html', {'cities': cities, 'categories': categories})

# Edit Product View
@login_required
def edit_product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id, user=request.user)
    
    if request.method == 'POST':
        product.title = request.POST.get('name')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')
        product.phone_number = request.POST.get('phone_number')
        
        city_id = request.POST.get('city')
        category_id = request.POST.get('category')
        subcategory_id = request.POST.get('subcategory')
        
        if city_id:
            product.city_id = city_id
        if category_id:
            product.category_id = category_id
        if subcategory_id:
            product.subcategory_id = subcategory_id if subcategory_id else None
            
        product.save()
        
        images = request.FILES.getlist('images')
        for img in images:
            ProductImage.objects.create(product=product, image=img)
            
        return redirect('my_ads')
        
    cities = City.objects.all()
    categories = Category.objects.all()
    subcategories = SubCategory.objects.filter(category=product.category) if product.category else []
    return render(request, 'core/edit_product.html', {'product': product, 'cities': cities, 'categories': categories, 'subcategories': subcategories})

# Delete Product View
@login_required
def delete_product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id, user=request.user)
    product.delete()
    return redirect('my_ads')

# Settings View
@login_required
def settings_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        
        profile.whatsapp_number = request.POST.get('whatsapp_number', '')
        profile.home_address = request.POST.get('home_address', '')
        
        theme = request.POST.get('theme_preference')
        if theme:
            profile.theme_preference = theme
            
        profile.save()
        return redirect('settings')
        
    context = {'profile': profile}
    return render(request, 'core/settings.html', context)