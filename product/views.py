from django.shortcuts import render
from product.models import *

# Create your views here.

def product_list(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'product/product-list.html', context)

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    context = {
        'product': product,
    }
    return render(request, 'product/product-details.html', context)

def product_grid(request):
    return render(request, 'product/product-grid.html')