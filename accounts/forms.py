from django import forms
from .models import User, Vendor


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Password and Confirm Password does not match")

        return cleaned_data


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['vendor_name','vendor_license']