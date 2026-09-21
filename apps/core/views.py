from django.shortcuts import render
from apps.products.models import Product


def home(request):
    featured_products = Product.objects.filter(is_featured=True)

    return render(
        request,
        'core/home.html',
        {
            'featured_products': featured_products
        }
    )