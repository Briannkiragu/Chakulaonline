from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from .context_processors import get_cart_counter, get_cart_amounts, _get_cart_count_value

from menu.models import Category, Item
from vendor.models import Vendor, OpeningHour
from django.db.models import Prefetch
from .models import Cart
from django.contrib.auth.decorators import login_required
from  datetime import date, datetime
from orders.forms import OrderForm
from accounts.models import UserProfile



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

    opening_hours = OpeningHour.objects.filter(vendor=vendor).order_by('day', 'from_hour')
#check current day opening hours
    today_date = date.today()
    today = today_date.isoweekday()

    current_opening_hours = OpeningHour.objects.filter(vendor=vendor, day=today)
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        # ensure cart_count is defined for authenticated users
        cart_count = _get_cart_count_value(request)
    else:
        cart_count = 0

    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_count': cart_count,
        'cart_items': cart_items if request.user.is_authenticated else Cart.objects.none(),
        'opening_hours': opening_hours,
        'current_opening_hours' : current_opening_hours,
    }
    return render(request, 'marketplace/vendor_detail.html', context)

def add_to_cart(request, item_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # check if fooditem exists
            try:
                item = Item.objects.get(id=item_id)
                #check if usser has already added food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, item=item)

                    #increase cart quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status': 'success', 'message': 'Increased the cart quantity', 'cart_counter': _get_cart_count_value(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})

                except:
                    chkCart = Cart.objects.create(user=request.user, item=item, quantity=1)
                    return JsonResponse({'status': 'success', 'message': 'Added the item to  cart', 'cart_counter': _get_cart_count_value(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})

            except:
                return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)        
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'}, status=401)


def decrease_cart(request, item_id):
    # Logic to decrease the cart item quantity
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
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
                    return JsonResponse({'status': 'success', 'cart_counter': _get_cart_count_value(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
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
            'cart_count': _get_cart_count_value(request),
        }
        return render(request, 'marketplace/cart.html', context)
    else:
        return HttpResponse("You need to be logged in to view the cart.")\


def delete_cart(request, item_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                item = Item.objects.get(id=item_id)
                try:
                    chkCart = Cart.objects.get(user=request.user, item=item)
                    chkCart.delete()
                    return JsonResponse({'status': 'success', 'message': 'Item removed from cart', 'cart_counter': _get_cart_count_value(request), 'cart_amount': get_cart_amounts(request)})
                except:
                    return JsonResponse({'status': 'error', 'message': 'Item not in cart'}, status=404)
            except:
                return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'}, status=401)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            items = Item.objects.filter(item_name__icontains=keyword, is_available=True)
            item_count = items.count()
            context = {
                'items': items,
                'item_count': item_count,
            }
            return render(request, 'marketplace/search.html', context)
        else:
            return render(request, 'marketplace/search.html')
    else:
        return render(request, 'marketplace/search.html')

def search(request):
    address = request.GET['address']
    keyword = request.GET['keyword']
    latitude = request.GET['latitude']
    longitude = request.GET['longitude']
    radius = request.GET['radius']


    #get vendor id that has the fooditem the user is looking for
    fetch_vendors_by_fooditems = Item.objects.filter(item_name__icontains=keyword, is_available=True).values_list('vendor', flat=True)

    vendors = Vendor.objects.filter(id__in=fetch_vendors_by_fooditems) | Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True)
    
     
    vendor_count = vendors.count()
    context = {
         'vendors': vendors,
         'vendor_count': vendor_count,
     }
    return render(request, 'marketplace/listings.html', context)
@login_required(login_url='login')
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')
    user_profile = UserProfile.objects.get(user=request.user)
    default_values = {
        'first_name' : request.user.first_name,
        'last_name' : request.user.last_name,
        'phone' : request.user.phone_number,
        'email' : request.user.email,
        'address' : user_profile.address,
        'country' : user_profile.country,
        'state' : user_profile.state,
        'city' : user_profile.city,
        'pin_code' : user_profile.pin_code,
    }
    form = OrderForm(initial=default_values)
    context = {
        'form': form,
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/checkout.html', context)