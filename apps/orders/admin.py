from django.contrib import admin
from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'customer_name',
        'total_amount',
        'payment_status',
        'order_status',
        'created_at',
    )

    list_filter = (
        'payment_status',
        'order_status',
        'created_at',
    )

    search_fields = (
        'customer_name',
        'user__username',
        'user__email',
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'order',
        'product',
        'quantity',
        'price',
    )

    search_fields = (
        'product__name',
        'order__id',
    )
