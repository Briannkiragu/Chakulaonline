from .models import Cart
from menu.models import Item


def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            if cart_items:
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
            else:
                cart_count = 0

        except:
            cart_count = 0
    return dict(cart_count=cart_count)


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
