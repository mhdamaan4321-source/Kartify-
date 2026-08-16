from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from .models import Product, City, Category, Subcategory, ProductImage, ChatMessage

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

# Custom Logout View (Fixes HTTP 405 error completely)
def custom_logout(request):
    logout(request)
    return redirect('home')

# AJAX view to load subcategories dynamically based on selected category
def load_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)

# Home Page View (Search + Category Filter + City Filter)
def home_view(request):
    products = Product.objects.all().order_by('-id')
    cities = City.objects.all()
    categories = Category.objects.all()
    
    # Search Filter
    query = request.GET.get('q')
    if query:
        products = products.filter(title__icontains=query)
        
    # City Filter
    city_id = request.GET.get('city')
    if city_id:
        products = products.filter(city_id=city_id)
        
    # Category Filter
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
        
    context = {
        'products': products,
        'cities': cities,
        'categories': categories,
        'search_query': query if query else '',
        'selected_city': city_id if city_id else '',
        'selected_category': category_id if category_id else '',
    }
    return render(request, 'core/home.html', context)

# Product Detail View (Updated with Similar Ads)
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    # Ore category-la irukkira ana oru 4 similar products-ah edukka:
    similar_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:4]
    
    context = {
        'product': product,
        'similar_products': similar_products,
    }
    return render(request, 'core/product_detail.html', context)

# User Registration View
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

# My Ads View (Shows logged-in user's products)
@login_required
def my_ads_view(request):
    products = Product.objects.filter(user=request.user).order_by('-id')
    return render(request, 'core/my_ads.html', {'products': products})

# Add Product View (With Multiple Images & Subcategory Support)
@login_required
def add_product_view(request):
    if request.method == 'POST':
        product = Product.objects.create(
            user=request.user,
            title=request.POST.get('name'),
            price=request.POST.get('price'),
            description=request.POST.get('description'),
            phone_number=request.POST.get('phone_number'),
            city_id=request.POST.get('city'),
            category_id=request.POST.get('category'),
            subcategory_id=request.POST.get('subcategory')
        )
        
        # Save multiple images
        images = request.FILES.getlist('images')
        for img in images:
            ProductImage.objects.create(product=product, image=img)
            
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
            product.subcategory_id = subcategory_id
            
        product.save()
        
        images = request.FILES.getlist('images')
        for img in images:
            ProductImage.objects.create(product=product, image=img)
            
        return redirect('my_ads')
        
    cities = City.objects.all()
    categories = Category.objects.all()
    subcategories = Subcategory.objects.filter(category=product.category) if product.category else []
    return render(request, 'core/edit_product.html', {'product': product, 'cities': cities, 'categories': categories, 'subcategories': subcategories})

# Delete Product View
@login_required
def delete_product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id, user=request.user)
    product.delete()
    return redirect('my_ads')