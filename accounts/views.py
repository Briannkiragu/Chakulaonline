from django.shortcuts import redirect, render
from .forms import VendorForm
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages, auth
from django.contrib.auth import authenticate
from .utils import detectUser 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
# Create your models here.


#restrict vendor from acessing cust page
#restrict cust from acessing vendor page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied  
    
    
def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            #Create user using the form
        
           # user = form.save(commit=False)#ready to save but not yet saved to database
           # user.set_password(form.cleaned_data['password'])#hash the password
            #user.role = User.CUSTOMER
            #user.save()
            #messages.success(request, 'User registered successfully.')
            #return redirect('registerUser')
            
            #create user using create_user method
            first_Name = form.cleaned_data['first_name']
            last_Name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_Name, last_name=last_Name, username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, 'User registered successfully.')
            return redirect('registerUser')
        else: 
            print('Invalid form data')  
            print(form.errors)

    else:
         form = UserForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/registerUser.html', context)

def registerVendor(request):
    if request.method == 'POST':
        #Store the data and create the user
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_Name = form.cleaned_data['first_name']
            last_Name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(
                first_name=first_Name,
                last_name=last_Name,
                username=username,
                email=email,
                password=password,
            )
            user.role = User.VENDOR
            user.save()

            vendor = v_form.save(commit=False)
            vendor.user = user
            vendor.save()

            messages.success(request, 'Vendor registered successfully.')
            return redirect('registerVendor')
        else:
            # Re-render with bound forms so you can see validation errors
            print('invalid form')
            print(form.errors)
            print(v_form.errors)
    else:
        form = UserForm()
        v_form = VendorForm()

    context = {
        'form': form,
        'v_form': v_form,
    }
    return render(request, 'accounts/registerVendor.html', context)



def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in.')
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.filter(email=email).first()
       
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, 'You are now logged out.')
    return redirect('login')
@login_required(login_url='login')
def myAccount(request):
    
   user = request.user
   redirectUrl = detectUser(user)
   return redirect(redirectUrl)


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, 'accounts/custDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')