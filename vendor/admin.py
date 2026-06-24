from django.contrib import admin
from vendor.models import Vendor

# Register your models here.
class VendorAdmin(admin.ModelAdmin):
    list_display = ('vendor_name', 'user', 'created_at', 'modified_at')
    list_display_links = ('vendor_name', 'user')
    


admin.site.register(Vendor, VendorAdmin)
