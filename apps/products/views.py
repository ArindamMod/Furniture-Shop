from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    return render(
        request,
        'products/product_detail.html',
        {
            'product': product
        }
    )


def category_products(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = category.products.all()

    return render(
        request,
        'products/category_products.html',
        {
            'category': category,
            'products': products
        }
    )
