from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse
from .models import Product, Category, Review, Order, OrderItem
from .forms import CheckoutForm, ReviewForm
from .cart import add, remove, set_qty, items_and_total

def theme_toggle(request, mode:str):
    mode = 'dark' if mode.lower().startswith('d') else 'light'
    resp = redirect(request.META.get('HTTP_REFERER') or 'home')
    resp.set_cookie('theme', mode, max_age=60*60*24*365, samesite='Lax')
    return resp

def home(request):
    featured = Product.objects.filter(is_featured=True).prefetch_related('images')[:6]
    reviews = Review.objects.filter(status='APPROVED').select_related('product').order_by('-created_at')[:4]
    categories = Category.objects.all()
    return render(request, 'store/home.html', {
        'featured': featured,
        'reviews': reviews,
        'categories': categories
    })

def shop(request):
    products = Product.objects.all().select_related('category').prefetch_related('images').order_by('-created_at')
    return render(request, 'store/shop.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product.objects.prefetch_related('images','reviews'), slug=slug)
    approved_reviews = product.reviews.filter(status='APPROVED').order_by('-created_at')
    form = ReviewForm()
    if request.method == 'POST' and request.POST.get('action') == 'review':
        form = ReviewForm(request.POST)
        if form.is_valid():
            Review.objects.create(
                product=product,
                rating=form.cleaned_data['rating'],
                title=form.cleaned_data['title'],
                body=form.cleaned_data['body'],
                status='PENDING'
            )
            messages.success(request, "Thanks! Your review was submitted for moderation.")
            return redirect('product_detail', slug=product.slug)
    return render(request, 'store/product_detail.html', {'product': product, 'reviews': approved_reviews, 'form': form})

def cart_view(request):
    items, total = items_and_total(request.session)
    return render(request, 'store/cart.html', {'items': items, 'total': total})

def cart_add(request, product_id:int):
    product = get_object_or_404(Product, id=product_id)
    add(request.session, product.id, 1)
    messages.success(request, f"Added {product.name} to cart.")
    return redirect('cart')

def cart_remove(request, product_id:int):
    remove(request.session, product_id)
    messages.success(request, "Item removed from cart.")
    return redirect('cart')

def cart_update(request):
    if request.method == 'POST':
        for k, v in request.POST.items():
            if k.startswith('qty_'):
                pid = int(k.split('_',1)[1])
                try: qty = int(v)
                except ValueError: qty = 1
                set_qty(request.session, pid, max(0, qty))
        messages.success(request, "Cart updated.")
    return redirect('cart')

@transaction.atomic
def checkout(request):
    items, total = items_and_total(request.session)
    if not items:
        messages.error(request, "Your cart is empty.")
        return redirect('shop')
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                email=form.cleaned_data['email'],
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                line1=form.cleaned_data['line1'],
                line2=form.cleaned_data['line2'],
                city=form.cleaned_data['city'],
                region=form.cleaned_data['region'],
                postal_code=form.cleaned_data['postal_code'],
                country=form.cleaned_data['country'],
                status='PENDING_COD',
                payment_method='COD',
                total_pkr=total
            )
            for it in items:
                OrderItem.objects.create(
                    order=order, product=it.product,
                    name=it.product.name, price_pkr=it.product.price_pkr, quantity=it.quantity
                )
                if it.product.stock >= it.quantity:
                    it.product.stock -= it.quantity
                    it.product.save(update_fields=['stock'])
            request.session['cart'] = {}
            request.session.modified = True
            return redirect('order_success', order_id=order.id)
    else:
        form = CheckoutForm()
    return render(request, 'store/checkout.html', {'items': items, 'total': total, 'form': form})

def order_success(request, order_id:int):
    order = get_object_or_404(Order.objects.prefetch_related('items'), id=order_id)
    return render(request, 'store/order_success.html', {'order': order})

def about(request): return render(request, 'store/about.html')
def contact(request): return render(request, 'store/contact.html')
def shipping_policy(request): return render(request, 'store/policies/shipping.html')
def returns_policy(request): return render(request, 'store/policies/returns.html')
def privacy_policy(request): return render(request, 'store/policies/privacy.html')
def terms(request): return render(request, 'store/policies/terms.html')