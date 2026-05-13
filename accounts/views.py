from django.shortcuts import redirect, render
from .forms import UserForm
from .models import User
from django.contrib import messages
# Create your models here.

def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)#ready to save but not yet saved to database
            user.set_password(form.cleaned_data['password'])#hash the password
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