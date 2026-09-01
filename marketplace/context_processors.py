from .models import Cart, Tax


def get_cart_counter(request):
    # keep for template context processor compatibility
    return dict(cart_count=_get_cart_count_value(request))


def get_cart_amounts(request):
    subtotal = 0
    tax = 0
    grand_total = 0
    tax_dict = {}
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for cart_item in cart_items:
            subtotal += cart_item.item.price * cart_item.quantity

        for current_tax in Tax.objects.filter(is_active=True):
            tax_amount = round((current_tax.tax_percentage * subtotal) / 100, 2)
            tax_dict[current_tax.tax_type] = {
                str(current_tax.tax_percentage): str(tax_amount),
            }
            tax += tax_amount
        grand_total = subtotal + tax

    return dict(subtotal=subtotal, tax=tax, grand_total=grand_total, tax_dict=tax_dict)


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
