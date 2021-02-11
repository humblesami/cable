from django.contrib import admin
from .models import Area, Package, PackageType, Client, Payment


class AreaAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'created_at']
    exclude = ['created_at',]


class PackageTypeAdmin(admin.ModelAdmin):
    list_display= ['name']
    search_fields = ['name']
    exclude = ['created_at']


class PackageAdmin(admin.ModelAdmin):
    list_display= ['name','status','package_type']
    search_fields = ['name', 'package_type']
    list_filter = ['package_type', 'status']
    exclude = ['created_at']


class ClientAdmin(admin.ModelAdmin):
    list_display = ['name','mobile','email','next_payment_date','price','status']
    search_fields = ['package']
    exclude = ['created_at']


class PaymentAdmin(admin.ModelAdmin):
    exclude = ['created_at']


admin.site.register(Area, AreaAdmin)
admin.site.register(PackageType,PackageTypeAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Client, ClientAdmin)
