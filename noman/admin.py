from django.contrib import admin
from .models import Area, Package, PackageType, Client, Subscription, Payment
from datetime import datetime


class AbstractAdmin(admin.ModelAdmin):

    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        if obj.pk:
            obj.updated_by_id = obj.user.id
            obj.updated_at = datetime.now()
        else:
            obj.created_by_id = obj.user.id
            obj.created_at = datetime.now()
        super().save_model(request, obj, form, change)


class AreaAdmin(AbstractAdmin):
    list_display = ['name', 'status', 'created_at']
    list_filter = ['status']

    def get_queryset(self, request):
        qs = Area.full.all()
        return qs


class PackageTypeAdmin(AbstractAdmin):
    list_display = ['name']
    search_fields = ['name']


class PackageAdmin(AbstractAdmin):
    list_display= ['name','package_type']
    search_fields = ['name', 'package_type']
    list_filter = ['package_type']


class ClientAdmin(AbstractAdmin):
    list_display = ['area', 'name','mobile','email', 'start_date', 'end_date', 'balance']
    search_fields = ['package', 'area']
    fields = ['area', 'name','mobile','email', 'cnic', 'start_date', 'end_date', 'balance']
    readonly_fields = ['start_date', 'end_date', 'balance', 'created_at', 'updated_at', 'created_by', 'updated_by']

    def start_date(self, obj):
        subscription = obj.subscriptions.last().subscription_set.last()
        return subscription.start_date or ''
    
    def end_date(self, obj):
        subscription = obj.subscriptions.last().subscription_set.last()
        return subscription.last_date or ''


class PaymentAdmin(AbstractAdmin):
    readonly_fields = ['renewal_start_date', 'renewal_end_date', 'created_at', 'updated_at', 'created_by', 'updated_by']


class SubscriptionAdmin(AbstractAdmin):
    readonly_fields = ['expiry_date', 'created_at', 'updated_at', 'created_by', 'updated_by']


admin.site.register(Area, AreaAdmin)
admin.site.register(PackageType,PackageTypeAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
