from django.shortcuts import render, redirect, get_object_or_404
from product.models import *
from product.forms import CommentForm

# Create your views here.

def product_list(request):
    products = Product.objects.annotate(avg_rating=Avg('comments__rating'))
    context = {
        'products': products,
    }
    return render(request, 'product/product-list.html', context)

def product_detail(request, pk):
    product = Product.objects.annotate(avg_rating=Avg('comments__rating')).get(pk=pk)
    comments = Comment.objects.filter(product=pk)
    if  request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product=product
            comment.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = CommentForm()

    context = {
        'product': product,
        'form': form,
        'comments': comments,
    }
    return render(request, 'product/product-details.html', context)

def product_grid(request):
    return render(request, 'product/product-grid.html')