from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Product, City, Category, ProductImage

# Home Page View (Search + Category Filter + City Filter)
def home_view(request):
    products = Product.objects.all().order_by('-id')
    cities = City.objects.all()
    categories = Category.objects.all()
    
    # Search Filter (Handles both 'title' or 'name' dynamically based on model)
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

# Product Detail View
def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'core/product_detail.html', {'product': product})

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

# Add Product View (With Multiple Images Support)
@login_required
def add_product_view(request):
    if request.method == 'POST':
        product = Product.objects.create(
            user=request.user,
            title=request.POST.get('name'), # Model uses 'title' for the product name
            price=request.POST.get('price'),
            description=request.POST.get('description'),
            phone_number=request.POST.get('phone_number'),
            city_id=request.POST.get('city'),
            category_id=request.POST.get('category')
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
        
        # Optional: update city and category if present in form
        city_id = request.POST.get('city')
        category_id = request.POST.get('category')
        if city_id:
            product.city_id = city_id
        if category_id:
            product.category_id = category_id
            
        product.save()
        
        # Add new images if uploaded during edit
        images = request.FILES.getlist('images')
        for img in images:
            ProductImage.objects.create(product=product, image=img)
            
        return redirect('my_ads')
        
    cities = City.objects.all()
    categories = Category.objects.all()
    return render(request, 'core/edit_product.html', {'product': product, 'cities': cities, 'categories': categories})

# Delete Product View
@login_required
def delete_product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id, user=request.user)
    product.delete()
    return redirect('my_ads')