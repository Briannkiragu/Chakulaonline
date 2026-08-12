from django.contrib import admin
from vendor.models import Vendor, OpeningHour

# Register your models here.
class VendorAdmin(admin.ModelAdmin):
    list_display = ('vendor_name', 'user', 'created_at', 'modified_at')
    list_display_links = ('vendor_name', 'user')

class OpeningHourAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'day', 'from_hour', 'to_hour', 'is_closed')
    list_filter = ('vendor', 'day')
    


admin.site.register(Vendor, VendorAdmin)
admin.site.register(OpeningHour, OpeningHourAdmin)
