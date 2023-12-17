# from django.shortcuts import render, get_object_or_404
# from products.models import Product

# # Create your views here.


# def get_product(request, slug):
#     try:
#         product = Product.objects.get(slug=slug)
#         return render(request, 'product/product.html', context={'product': product})

#     except Exception as e:
#         print(e)


from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from products.models import Product, SizeVarient
from accounts.models import Cart, CartItems
from django.http import HttpResponseRedirect


def get_product(request, slug):
    try:
        # Using get_object_or_404 to simplify the code
        product = get_object_or_404(Product, slug=slug)
        context = {'product': product}
        if request.GET.get('size'):
            size = request.GET.get('size')
            print(size)
            price = product.get_product_price_by_size(size)
            context['selected_size'] = size
            context['updated_price'] = price
            print(price)

        return render(request, 'product/products.html', context=context)
    

    except Http404:
        # Product not found, return a 404 response
        # You should have a custom 404 template
        return render(request, '404.html')

    except Exception as e:
        # Log the exception for debugging purposes
        print(e)
        # Return a generic error response or redirect to a specific page
        # You should have a custom error template
        return render(request, 'error.html')



    