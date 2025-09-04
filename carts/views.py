from django.shortcuts import render, redirect
from store.models import Product
from .models import Cart, CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    try:
        cart = Cart.objects.get(cart_id = _cart_id(request)) #getting the cart object based on the cart_id from the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart) #getting the cart item based on the product and cart
        if cart_item.quantity < cart_item.product.stock: #checking if the quantity is less than the stock
            cart_item.quantity += 1 #if yes then increment the quantity by 1
        cart_item.save()

    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart
        )
        cart_item.save()
     
    return redirect('cart') #redirecting to the cart page after adding the product to the cart

def minus_cart(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request)) #getting the cart object based on the cart_id from the session
    product = get_object_or_404(Product, id=product_id) #getting the product object based on the product_id from the url
    cart_item = CartItem.objects.get(product=product, cart=cart) #getting the cart item based on the product and cart
    if cart_item.quantity > 1: #checking if the quantity is greater than 1
        cart_item.quantity -= 1 #if yes then decrement the quantity by 1
        cart_item.save()
    else:
        cart_item.delete() #if no then delete the cart item
    return redirect('cart') #redirecting to the cart page after removing the product from the cart

def checkout(request):
    return render(request, 'store/checkout.html')

def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request)) #getting the cart object based on the cart_id from the session
    product = get_object_or_404(Product, id=product_id) #getting the product object based on the product_id from the url
    cart_item = CartItem.objects.get(product=product, cart=cart) #getting the cart item based on the product and cart
    cart_item.delete() #deleting the cart item
    return redirect('cart') #redirecting to the cart page after removing the product from the cart  

def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) #getting the cart object based on the cart_id from the session
        cart_items = CartItem.objects.filter(cart=cart, isactive=True) #getting the cart items based on the cart and isactive=True
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity = cart_item.quantity
        C_GST = (5 * total)/100
        S_GST = (5 * total)/100
        grand_total = total + C_GST + S_GST
    except Exception as e:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'C_GST': C_GST,
        'S_GST': S_GST,
        'grand_total': round(grand_total,2),
    }

    return render(request, 'store/carts.html', context)