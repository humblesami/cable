from django.contrib import admin
from .models import Area, Package, PackageType, Client, ClientPackage, Subscription, Payment
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

    def changelist_view(self, request, extra_context=None):
        status = request.GET.get('status__exact')
        if status == None:
            q = request.GET.copy()
            q['status__exact'] = 1
            request.GET = q
            request.META['QUERY_STRING'] = request.GET.urlencode()
        else:
            q = request.GET.copy()
            if q.get('status__exact'):
                del q['status__exact']
            request.GET = q
            request.META['QUERY_STRING'] = request.GET.urlencode()
        return super().changelist_view(request, extra_context=extra_context)


class PackageTypeAdmin(AbstractAdmin):
    list_display= ['name']
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
        client_package = obj.clientpackage_set.all()
        if client_package:
            client_package = list(client_package)[-1]
            subscription = client_package.subscription_set.all()
            if subscription:
                subscription = list(subscription)[-1]
                return subscription.start_date
        return ''
    
    def end_date(self, obj):
        client_package = obj.clientpackage_set.all()
        if client_package:
            client_package = list(client_package)[-1]
            subscription = client_package.subscription_set.all()
            if subscription:
                subscription = list(subscription)[-1]
                return subscription.end_date
        return ''


class PaymentAdmin(AbstractAdmin):
    pass


class SubscriptionAdmin(AbstractAdmin):
    pass


class ClientPackageAdmin(AbstractAdmin):
    pass


admin.site.register(Area, AreaAdmin)
admin.site.register(PackageType,PackageTypeAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(ClientPackage, ClientPackageAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
