from .models import Cart
from menu.models import Item


def get_cart_counter(request):
    # keep for template context processor compatibility
    return dict(cart_count=_get_cart_count_value(request))


def get_cart_amounts(request):
    subtotal = 0
    tax_data = 0
    grand_total = 0
    tax_dict = {}
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            for cart_item in cart_items:
                food_item = Item.objects.get(pk=cart_item.food_item.id)
                subtotal += (cart_item.food_item.price * cart_item.quantity)
            tax_percentage = 2
            tax_data = (tax_percentage * subtotal)/100
            grand_total = subtotal + tax_data

            tax_dict.update({'tax_percentage': tax_percentage, 'tax_data': tax_data, 'subtotal': subtotal, 'grand_total': grand_total})
        except:
            pass
    return dict(subtotal=subtotal, tax=tax_data, grand_total=grand_total, tax_dict=tax_dict)


def _get_cart_count_value(request):
    """Return integer cart count for a given request.

    This helper is used by views that expect an integer and by the
    context processor which needs to return a dict.
    """
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except:
            cart_count = 0
    return cart_count
