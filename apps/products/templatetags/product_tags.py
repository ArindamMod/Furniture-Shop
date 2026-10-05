from django import template

register = template.Library()


@register.filter
def product_image(product):
    if product.image:
        filename = product.image.name.split('/')[-1]
        return f'images/products/{filename}'
    return ''