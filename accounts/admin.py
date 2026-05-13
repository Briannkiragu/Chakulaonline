from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile
# Register your models here.

class customUserAdmin(UserAdmin):
    #display the fields in the admin panel
    list_display= ('email','first_name','last_name','username','last_login','is_active')
    ordering=('-date_joined',)#hyphen is used to order the data in descending order
    filter_horizontal= ()
    list_filter=()
    fieldsets=()    

admin.site.register(User, customUserAdmin)
admin.site.register(UserProfile)