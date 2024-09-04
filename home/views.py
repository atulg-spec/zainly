from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from dashboard.models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from dashboard.forms import ContactForm
import random
import string
User = get_user_model()
# -=--------=---=----------=--=------PAGES--=---=------=---
# CONTACT US
@login_required
def contact(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        user = form.save()
        messages.success(request,'We will contact to you as soon as possible')
    return render(request,"home/contact.html")

# ABOUT
def about(request):
    return render(request,"home/about.html")

def disclaimer(request):
    return render(request,"home/disclaimer.html")

# POLICY
def privacypolicy(request):
    return render(request,"home/privacypolicy.html")

def refundpolicy(request):
    return render(request,"home/refundpolicy.html")

def termsofuse(request):
    return render(request,"home/termsofuse.html")

# END PAGES
def index(request):
    categories = Categories.objects.all()
    new_products = Product.objects.filter(keywords__keyword__icontains='New').order_by('-id').distinct()[:30]
    top_products = Product.objects.filter(keywords__keyword__icontains='Top').order_by('-id').distinct()[:30]
    sale_products = Product.objects.filter(keywords__keyword__icontains='Sale').order_by('-id').distinct()[:30]
    context = {
        'categories':categories,
        'new_products':new_products,
        'top_products':top_products,
        'sale_products':sale_products,
    }
    return render(request,'home/index.html',context)

def search(request,search):
    query = search
    products = Product.objects.none()
    if query:
        products = Product.objects.filter(
            models.Q(category__category__icontains=query) |  # Correct usage for ManyToManyField
            models.Q(description__icontains=query) |
            models.Q(keywords__keyword__icontains=query)
        ).distinct()[:100] 
    context = {
        'products':products,
        'search':search,
    }
    return render(request,'home/search.html',context)

def product_view(request,id):
    product = Product.objects.filter(id=id).first()
    product_images = ProductImage.objects.filter(product=product)
    stars = [i for i in range(0,product.stars)]
    categories = Categories.objects.all()
    query = product.category.first().category
    related_products = Product.objects.none()
    if query:
        related_products = Product.objects.filter(
            models.Q(category__category__icontains=query) |  # Correct usage for ManyToManyField
            models.Q(description__icontains=query) |  # This is fine as description is a text field
            models.Q(keywords__keyword__icontains=query)  # Correct usage for ManyToManyField
        ).distinct()[:100]  # Use distinct() to avoid duplicate results if there are multiple matches

    context = {
        'related_products':related_products,
        'categories':categories,
        'stars':stars,
        'product_images':product_images,
        'product':product,
    }
    return render(request,'home/product-view.html',context)

@login_required
def add_to_cart(request,id,size,qty):
    product = Product.objects.filter(id=id).first()
    selected_size = Sizes.objects.filter(size=size).first()
    if product:
        exist = Cart.objects.filter(user=request.user,product=product).first()
        if not exist:
            Cart.objects.create(user=request.user,size=selected_size,product=product,quantity=qty)
    return redirect('/cart')

@login_required
def remove_item(request,id):
    product = Cart.objects.filter(user=request.user,id=id).first()
    if product:
        product.delete()
    return redirect('/cart')

@login_required
def increase_quantity(request,id):
    product = Cart.objects.filter(user=request.user,id=id).first()
    if product:
        product.quantity = product.quantity + 1
        product.save()
    return redirect('/cart')

@login_required
def decrease_quantity(request,id):
    product = Cart.objects.filter(user=request.user,id=id).first()
    if product:
        try:
            if product.quantity < 2:
                messages.error(request,"Quantity can't be less than 1")
            else:
                product.quantity = product.quantity - 1
                product.save()
        except:
            messages.info(request,'Invalid details')
    return redirect('/cart')

@login_required
def cart(request):
    trending_products = Product.objects.filter(keywords__keyword__icontains='Trending').order_by('-id').distinct()[:6]
    cart_items = Cart.objects.filter(user=request.user).filter(ordered=False)
    categories = Categories.objects.all()
    total = 0
    for x in cart_items:
        total = total + x.product.price * x.quantity
    context = {
        'trending_products':trending_products,
        'categories':categories,
        'total':total,
        'cart_items':cart_items,
    }
    return render(request,'home/cart.html',context)

@login_required
def create_order(request):
    trending_products = Product.objects.filter(keywords__keyword__icontains='Trending').order_by('-id').distinct()[:6]
    cart_items = Cart.objects.filter(user=request.user).filter(ordered=False)
    order = Order.objects.create(user=request.user)
    order.products.set(cart_items)  # Use set() to assign the cart_items to the products field
    categories = Categories.objects.all()
    context = {
        'trending_products':trending_products,
        'categories':categories,
    }
    return redirect('/my-orders')

@login_required
def my_orders(request):
    trending_products = Product.objects.filter(keywords__keyword__icontains='Trending').order_by('-id').distinct()[:6]
    orders = Order.objects.filter(user=request.user)
    categories = Categories.objects.all()
    print(orders)
    context = {
        'trending_products':trending_products,
        'categories':categories,
        'orders':orders,
    }
    return render(request,'home/orders.html',context)

def categories(request):
    trending_products = Product.objects.filter(keywords__keyword__icontains='Trending').distinct()[:50]
    categories = Categories.objects.all()
    context = {
        'trending_products':trending_products,
        'categories':categories,
    }
    return render(request,'home/categories.html',context)

@login_required
def track_order(request,id):
    trending_products = Product.objects.filter(keywords__keyword__icontains='Trending').order_by('-id').distinct()[:6]
    order = Order.objects.filter(user=request.user,order_id=id).first()
    categories = Categories.objects.all()
    context = {
        'trending_products':trending_products,
        'categories':categories,
        'order':order,
    }
    return render(request,'home/track_order.html',context)

def search_suggestions(request):
    query = request.GET.get('q', '')
    suggestions = Keywords.objects.none()
    if query:
        suggestions = Keywords.objects.filter(
            models.Q(keyword__icontains=query)
        ).reverse()        
    results = [
        s.keyword for s in suggestions if s.keyword
    ][:30]
    return JsonResponse(results, safe=False)

@csrf_exempt  # Use this only if you're not using {% csrf_token %} in the form, otherwise remove it
@login_required
def save_address(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pin_code = request.POST.get('pin_code')
        address = request.POST.get('address')
        user = User.objects.filter(email=request.user.email).first()
        user.phone_number = phone_number
        user.city = city
        user.state = state
        user.pin_code = pin_code
        user.address = address
        user.save()
        return JsonResponse({'status': 'success', 'message': 'Address saved successfully!'})
    else:
        return JsonResponse({'status': 'fail', 'message': 'Invalid request method.'}, status=405)
