from django.contrib import admin
from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price',
        'is_featured',
        'created_at',
    )

    list_filter = (
        'category',
        'is_featured',
    )

    search_fields = (
        'name',
        'description',
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )

    search_fields = (
        'name',
    )