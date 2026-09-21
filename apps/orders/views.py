from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
import razorpay
from decouple import config
from apps.cart.models import Cart
from .models import Order, OrderItem

client = razorpay.Client(
    auth=(
        config('RAZORPAY_KEY_ID'),
        config('RAZORPAY_KEY_SECRET')
    )
)

@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    if not cart.items.exists():
        return redirect('cart')

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')

        total = sum(
            item.product.price * item.quantity
            for item in cart.items.all()
        )

        order = Order.objects.create(
            user=request.user,
            customer_name=customer_name,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            total_amount=total,
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

        razorpay_order = client.order.create(
            {
                'amount': int(total * 100),
                'currency': 'INR',
                'payment_capture': 1,
            }
        )
        order.razorpay_order_id = razorpay_order['id']
        order.save(update_fields=['razorpay_order_id'])

        return render(
        request,
        'orders/checkout.html',
        {
            'cart': cart,
            'total': total,
            'razorpay_key_id': config('RAZORPAY_KEY_ID'),
            'razorpay_order_id': razorpay_order['id'],
            'order_id': order.id,

            'customer_name': customer_name,
            'address': address,
            'city': city,
            'state': state,
            'pincode': pincode,
        }
        )

    total = sum(
        item.product.price * item.quantity
        for item in cart.items.all()
    )

    return render(
        request,
        'orders/checkout.html',
        {
            'cart': cart,
            'total': total,
        }
    )

@login_required
def verify_payment(request):

    if request.method != 'POST':
        return JsonResponse(
            {'success': False, 'message': 'Invalid request.'},
            status=400
        )

    order_id = request.POST.get('order_id')
    razorpay_order_id = request.POST.get('razorpay_order_id')
    razorpay_payment_id = request.POST.get('razorpay_payment_id')
    razorpay_signature = request.POST.get('razorpay_signature')

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    if order.razorpay_order_id != razorpay_order_id:
        return JsonResponse(
            {'success': False, 'message': 'Invalid order.'},
            status=400
        )

    try:

        client.utility.verify_payment_signature(
            {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature,
            }
        )

    except razorpay.errors.SignatureVerificationError:

        order.payment_status = 'failed'
        order.save(update_fields=['payment_status'])

        return JsonResponse(
            {
                'success': False,
                'message': 'Payment verification failed.'
            },
            status=400
        )

    order.payment_status = 'paid'
    order.order_status = 'confirmed'
    order.razorpay_payment_id = razorpay_payment_id

    order.save(
        update_fields=[
            'payment_status',
            'order_status',
            'razorpay_payment_id',
        ]
    )

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart.items.all().delete()

    return JsonResponse(
        {
            'success': True,
            'order_id': order.id
        }
    )

@login_required
def order_success(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        'orders/order_success.html',
        {
            'order': order
        }
    )

@login_required
def my_orders(request):
    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'orders/my_orders.html',
        {
            'orders': orders
        }
    )

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        'orders/order_detail.html',
        {
            'order': order
        }
    )