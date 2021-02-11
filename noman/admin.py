from django.contrib import admin
from .models import Area, Package, PackageType, Client, ClientPackage, Subscription, Payment


class AreaAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'created_at']
    exclude = ['created_at',]


class PackageTypeAdmin(admin.ModelAdmin):
    list_display= ['name']
    search_fields = ['name']
    exclude = ['created_at']


class PackageAdmin(admin.ModelAdmin):
    list_display= ['name','package_type']
    search_fields = ['name', 'package_type']
    list_filter = ['package_type']
    exclude = ['created_at']


class ClientAdmin(admin.ModelAdmin):
    list_display = ['area', 'name','mobile','email']
    search_fields = ['package', 'area']
    exclude = ['created_at']


class PaymentAdmin(admin.ModelAdmin):
    exclude = ['created_at']


class SubscriptionAdmin(admin.ModelAdmin):
    exclude = ['end_date']


admin.site.register(Area, AreaAdmin)
admin.site.register(PackageType,PackageTypeAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(ClientPackage)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
