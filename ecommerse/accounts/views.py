from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import Profile

from products.models import Coupon, Product, SizeVarient
from accounts.models import Cart, CartItems
# Create your views here.

def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=email)

        if not user_obj.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)

        print(user_obj[0],  "==================================>")

        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'Your accout is not varified')
            return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(username=email, password=password)
        if user_obj:
            login(request, user_obj)
            return redirect('/')

        messages.warning(request, 'Invalid credentials')
        return HttpResponseRedirect(request.path_info)

    return render(request, 'account/login.html')


def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=email)
        if user_obj.exists():
            messages.warning(request, 'Email is already teken.')
            return HttpResponseRedirect(request.path_info)
        print(email)
        user_obj = User.objects.create(
            first_name=first_name, last_name=last_name, email=email, username=email)
        user_obj.set_password(password)
        user_obj.save()

        messages.success(request, 'An email has been sent on your mail.')
        return HttpResponseRedirect(request.path_info)
    return render(request, 'account/register.html')


def activate_email(request, email_token):
    print(email_token , "==================================>")
    try:
        user = Profile.objects.get(email_token=email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/')
    except Exception as e:
        return HttpResponse('Invalid Email token')


def add_to_cart(request, uid):
    varient = request.GET.get('varient')

    product = Product.objects.get(uid=uid)
    user = request.user
    cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)

    cart_item = CartItems.objects.create(cart=cart, product=product)
    if varient:
        varient = request.GET.get('varient') 
        size_varient = SizeVarient.objects.get(size_name=varient)
        cart_item.size_varient.add(size_varient)
        cart_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_cart(request, cart_item_uid):
    try:
        cart_item = CartItems.objects.get(uid=cart_item_uid)
        cart_item.delete()
    except CartItems.DoesNotExist:
        pass

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart(request):
    user_cart = Cart.objects.filter(user=request.user, is_paid=False).first()
    
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(coupon_code__icontains=coupon_code).first()

        if not coupon_obj:
            messages.warning(request, 'Invalid Coupon.')
            print("Invalid Coupon") 
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if user_cart.coupon:
            messages.warning(request, 'Coupon already exists.')
            print('Coupon already exists.') 
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user_cart.coupon = coupon_obj
        user_cart.save()
        messages.success(request, 'Coupon Applied.')
        print('Coupon Applied.') 
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    context = {'cart': user_cart}   
    return render(request, 'account/cart.html', context=context)



def continue_shopping(request):
    return render(request, 'home/index.html')