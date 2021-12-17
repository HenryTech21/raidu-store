from django.shortcuts import render
from django.http import JsonResponse

import json
import datetime

from .models import *
from . utils import cookieCart, cartData, guestOrder

# Create your views here.

def home(request):

    data = cartData(request)

    cartItems = data['cartItems']

    products = Product.objects.all()
    blogs = BlogPost.objects.all()
    context = {'products': products, 'cartItems':cartItems, 'blogs': blogs}
    return render(request, 'store/home.html', context)


def slider(request):

    return render(request, 'store/slider.html')


def about(request):

    return render(request, 'store/about.html')


def store(request):
   
    data = cartData(request)
    cartItems = data['cartItems']
        
    products = Product.objects.all()
    context = {'products': products, 'cartItems':cartItems} 
               
    return render(request, 'store/store.html', context)


def view_product(request,pk):
    
    data = cartData(request)
    cartItems = data['cartItems']
    
    product = Product.objects.get(id=pk)
    context = {'product': product, 'cartItems':cartItems}      
    return render(request, 'store/view_product.html', context)


def cart(request):

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    context = {'items': items, 'order': order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('ProductId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete = False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity +1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity -1 )

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    if action == 'delete':
        orderItem.delete()

    return JsonResponse('item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True

    order.save()

    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address = data['shipping']['address'],
        city = data['shipping']['city'],
        state = data['shipping']['state'],
        zipcode = data['shipping']['zip']
    )

    return JsonResponse('Payment submitted', safe=False)

def orderSubmitted(request):

    return render(request, 'store/order_submitted.html')

def blogs(request):

	blogs = BlogPost.objects.all()

	context = {'blogs': blogs,}

	return render(request, 'store/blog.html', context)

def footer(request):

    return render(request, 'store/footer.html')

def viewPost(request, pk):

    data = cartData(request)

    cartItems = data['cartItems']

    blog = BlogPost.objects.get(id=pk)
    context = {'blog': blog, 'cartItems' :cartItems }

    cartItems = data['cartItems']

    return render(request, 'store/view_post.html', context)



