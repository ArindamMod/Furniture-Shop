from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.products.models import Product
from .models import Cart, CartItem


@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)

        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect('cart')

    return redirect('product_detail', product_id)


@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    total = sum(
        item.product.price * item.quantity
        for item in cart.items.all()
    )

    return render(
        request,
        'cart/cart.html',
        {
            'cart': cart,
            'total': total
        }
    )


@login_required
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(
            CartItem,
            id=item_id,
            cart__user=request.user
        )

        item.delete()

    return redirect('cart')

@login_required
def increase_quantity(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(
            CartItem,
            id=item_id,
            cart__user=request.user
        )

        item.quantity += 1
        item.save()

    return redirect('cart')

@login_required
def decrease_quantity(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(
            CartItem,
            id=item_id,
            cart__user=request.user
        )

        if item.quantity > 1:
            item.quantity -= 1
            item.save()

    return redirect('cart')

