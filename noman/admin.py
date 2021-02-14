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


class PackageTypeAdmin(admin.ModelAdmin):
    list_display= ['name']
    search_fields = ['name']
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


class PackageAdmin(admin.ModelAdmin):
    list_display= ['name','package_type']
    search_fields = ['name', 'package_type']
    list_filter = ['package_type']
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


class ClientAdmin(admin.ModelAdmin):
    list_display = ['area', 'name','mobile','email', 'start_date', 'end_date', 'balance']
    search_fields = ['package', 'area']
    fields = ['area', 'name','mobile','email', 'cnic', 'start_date', 'end_date', 'balance']
    readonly_fields = ['start_date', 'end_date', 'balance', 'created_at', 'updated_at', 'created_by', 'updated_by']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        if obj.pk:
            obj.updated_by_id = obj.user.id
            obj.updated_at = datetime.now()
        else:
            obj.created_by_id = obj.user.id
            obj.created_at = datetime.now()
        super().save_model(request, obj, form, change)
    
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
        # last=list(obj.clientpackage_set.all()[0].subscription_set.all())[-1]
        # return obj.client_package.subscription.start_date
    # user_address.short_description = 'User address'



class PaymentAdmin(admin.ModelAdmin):
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


class SubscriptionAdmin(admin.ModelAdmin):
    readonly_fields = ['end_date', 'created_at', 'updated_at', 'created_by', 'updated_by']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        if obj.pk:
            obj.updated_by_id = obj.user.id
            obj.updated_at = datetime.now()
        else:
            obj.created_by_id = obj.user.id
            obj.created_at = datetime.now()
        super().save_model(request, obj, form, change)

class ClientPackageAdmin(admin.ModelAdmin):
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


admin.site.register(Area, AreaAdmin)
admin.site.register(PackageType,PackageTypeAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(ClientPackage, ClientPackageAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
