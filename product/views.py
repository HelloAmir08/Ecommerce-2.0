from django.shortcuts import render

# Create your views here.

def product_list(request):
    return render(request, 'product/product-list.html')

def product_detail(request):
    return render(request, 'product/product-details.html')

def product_grid(request):
    return render(request, 'product/product-grid.html')