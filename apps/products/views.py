from django.shortcuts import get_object_or_404, render
from .models import Product, Category


def product_list(request):
    query = request.GET.get('q', '').strip()

    products = Product.objects.all()

    if query:
        products = products.filter(
            name__icontains=query
        ) | products.filter(
            description__icontains=query
        ) | products.filter(
            category__name__icontains=query
        )

    return render(
        request,
        'products/product_list.html',
        {
            'products': products.distinct(),
            'query': query,
        }
    )


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    return render(
        request,
        'products/product_detail.html',
        {'product': product}
    )


def category_products(request, pk):
    category = get_object_or_404(Category, pk=pk)

    products = category.products.all()

    return render(
        request,
        'products/category_products.html',
        {
            'category': category,
            'products': products,
        }
    )

def category_list(request):
    categories = Category.objects.all()

    return render(
        request,
        'products/category_list.html',
        {'categories': categories}
    )

