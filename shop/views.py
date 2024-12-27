from django.shortcuts import render, redirect,get_object_or_404
from .models import Category, Product, Cart, CartItem
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def store(request):
    context = {}
    return render(request, 'store.html')

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        
    return render(request,
                  'product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})

def product_detail(request, id, slug):
    category = None
    categories = Category.objects.all()
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    return render(request,
                  'product/detail.html',
                  {'category': category,
                   'categories': categories,
                    'product': product})
@require_POST
def cart_add(request, product_id):
    cart_id = request.session.get('cart_id')

    if cart_id:
        try:
            cart = Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            cart = Cart.objects.create()
    else:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id
    
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1

    cart_item.save()

    response_data = {
        'success':True,
        'message':f'Товар {product.name} был добавлен в корзину'
    }

    return JsonResponse(response_data)


def cart_detail(request):
    cart_id = request.session.get('cart_id')
    cart = None
    category = None
    categories = Category.objects.all()

    if cart_id:
        cart = get_object_or_404(Cart, id = cart_id)
    if not cart or not cart.items.exists():
        cart = None

    return render(request, 'cart.html', {'cart':cart, 'category': category,
                   'categories': categories})

def cart_remove(request, product_id):
    cart_id = request.session.get('cart_id')
    cart = get_object_or_404(Cart, id = cart_id)
    item = get_object_or_404(CartItem, id = product_id, cart = cart)
    item.quantity -= 1
    if item.quantity == 0:
        item.delete()
    else:
        item.save()

    return redirect('cart_detail')

def cart_increase(request, product_id):
    cart_id = request.session.get('cart_id')
    cart = get_object_or_404(Cart, id = cart_id)
    item = get_object_or_404(CartItem, id = product_id, cart = cart)
    item.quantity += 1
    item.save()

    return redirect('cart_detail')

def get_user(request):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        user = request.user
        print(user)
        return render(request, 'profile.html', {
        'user':user, 'categories': categories
    })
    else:
        return redirect('login')


def register_user(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form2 = SignUpForm(request.POST)
        if form2.is_valid():
           form2.save()
           username = form2.cleaned_data['username']
           password = form2.cleaned_data['password1']

           user = authenticate(username=username, password=password)
           login(request, user)
           messages.success(request, ('Вы были успешно зарегистрированы!'))
           return redirect('product_list')
        else:
            print(form2.errors.as_data())
            messages.success(request, ('Что-то пошло не так!'))
            return redirect('register')

    else:
        form2 = SignUpForm()
        return render(request, 'register.html', {
        'form2':form2,
        'categories': categories
    })

def logout_user(request):
    logout(request)
    return redirect('product_list')

def login_user(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('product_list')
        else:
            print(request.errors.as_data())
            messages.success(request, ('Что-то пошло не так!'))
            return redirect('register')
    else: 
        return render(request, 'login.html', {'categories': categories})

@login_required(login_url="login")
def update_user(request):
    user = request.user
    categories = Category.objects.all()
    form2 = SignUpForm(request.POST or None, instance = user)
    if form2.is_valid():
        form2.save()
        login(request, user)
        return redirect('get_user')
    return render(request, 'update.html', {'form2':form2, 'categories': categories})

@login_required(login_url="login")
def order_create(request):
    categories = Category.objects.all()
    cart = None
    cart_id = request.session.get('cart_id')
    user = request.user

    if cart_id:
        cart = Cart.objects.get(id=cart_id)

        if not cart or not cart.items.exists():
            return redirect('cart_detail')
        
    if request.method == 'POST':
        
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = user
            order.save()

            for item in cart.items.all():
                OrderItem.objects.create(
                    order = order,
                    product = item.product,
                    price = item.product.price,
                    quantity = item.quantity
                )
            cart.delete()
            del request.session['cart_id']
            return redirect('order_confirmation', order.id)
        else:
            return redirect('order_create')
    else:
        form = OrderCreateForm()
        return render(request, 'order_create.html', {
            'cart':cart,
            'form':form,
            'customer':user,
            'categories': categories,
        })

@login_required(login_url="login")
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    categories = Category.objects.all()
    return render(request, 'order_confirmation.html', {'order':order, 'categories': categories})

@login_required(login_url="login")
def past_orders(request):
    user_orders = Order.objects.filter(customer=request.user)
    user_order_items = OrderItem.objects.all()
    categories = Category.objects.all()

    return render(request, 'past_orders.html', {'user_orders':user_orders, 'user_order_items':user_order_items, 'categories': categories})