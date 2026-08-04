from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from .context_processors import get_cart_counter, get_cart_amounts

from menu.models import Category, Item
from vendor.models import Vendor
from django.db.models import Prefetch
from .models import Cart
from django.contrib.auth.decorators import login_required

# Create your views here.
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()

    context = {
        'vendors': vendors,
        'vendor_count': vendor_count,
    }
    return render(request, 'marketplace/listings.html', context)


def vendor_detail(request, vendor_slug):
    vendor = Vendor.objects.get(vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'items',
            queryset=Item.objects.filter(is_available=True),
            to_attr='available_items'


        ))
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_count = 0

    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_count': cart_count,
    }
    return render(request, 'marketplace/vendor_detail.html', context)

def add_to_cart(request, item_id):
    if request.user.is_authenticated:
        if request.is_ajax():
            # check if fooditem exists
            try:
                item = Item.objects.get(id=item_id)
                #check if usser has already added food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, item=item)

                    #increase cart quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status': 'success', 'message': 'Increased the cart quantity', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})

                except:
                    chkCart = Cart.objects.create(user=request.user, item=item, quantity=1)
                    return JsonResponse({'status': 'success', 'message': 'Added the item to  cart', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})

            except:
                return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)        
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'}, status=401)


def decrease_cart(request, item_id):
    # Logic to decrease the cart item quantity
    if request.user.is_authenticated:
        if request.is_ajax():
            try:
                item = Item.objects.get(id=item_id)
                try:
                    chkCart = Cart.objects.get(user=request.user, item=item)
                    if chkCart.quantity > 1:
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0  # Set quantity to 0 if the item is removed from the cart
                    return JsonResponse({'status': 'success', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    return JsonResponse({'status': 'error', 'message': 'Item not in cart'}, status=404)
            except:
                return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'}, status=401)


@login_required(login_url='login')
def cart (request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user).order_by('-created_at')
        context = {
            'cart_items': cart_items,
            'cart_count': get_cart_counter(request),
        }
        return render(request, 'marketplace/cart.html', context)
    else:
        return HttpResponse("You need to be logged in to view the cart.")\


def delete_cart(request, item_id):
    if request.user.is_authenticated:
        if request.is_ajax():
            try:
                item = Item.objects.get(id=item_id)
                try:
                    chkCart = Cart.objects.get(user=request.user, item=item)
                    chkCart.delete()
                    return JsonResponse({'status': 'success', 'message': 'Item removed from cart', 'cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amounts(request)})
                except:
                    return JsonResponse({'status': 'error', 'message': 'Item not in cart'}, status=404)
            except:
                return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'}, status=401)
