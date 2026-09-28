from django.shortcuts import get_object_or_404, render
from .models import Product, Category
from .recommender import get_recommendations

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

    other_products = Product.objects.exclude(
        pk=product.pk
    ).select_related('category')

    recommended_products = get_recommendations(
        product,
        other_products,
        limit=3
    )

    return render(
        request,
        'products/product_detail.html',
        {
            'product': product,
            'recommended_products': recommended_products,
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
            'products': products,
        }
    )

def category_list(request):

    categories = Category.objects.all()

    category_images = {
        'Living Room': 'Modern Sofa',
        'Bedroom': 'King Size Bed',
        'Dining': 'Dining Table',
        'Office': 'Office Desk',
    }

    category_cards = []

    for category in categories:

        image_product_name = category_images.get(category.name)

        image_product = None

        if image_product_name:
            image_product = Product.objects.filter(
                name=image_product_name,
                category=category
            ).first()

        category_cards.append({
            'category': category,
            'image_product': image_product,
        })

    return render(
        request,
        'products/category_list.html',
        {'category_cards': category_cards}
    )
