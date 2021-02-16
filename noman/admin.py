from django.contrib import admin, messages
from django.db import IntegrityError
from django.http import HttpResponseRedirect

from .models import Area, Package, PackageType, Client, Subscription, Payment
from datetime import datetime


class AbstractAdmin(admin.ModelAdmin):

    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',  # jquery
        )

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
    search_fields = ['name']
    list_filter = ['status']

    def get_queryset(self, request):
        qs = Area.full.all()
        return qs


class PackageTypeAdmin(AbstractAdmin):
    list_display = ['name']
    search_fields = ['name']


class PackageAdmin(AbstractAdmin):
    list_display= ['name', 'package_type']
    search_fields = ['name', 'package_type']
    list_filter = ['package_type']
    autocomplete_fields = ['package_type']


class ClientAdmin(AbstractAdmin):
    list_display = ['area', 'name','mobile','email', 'balance']
    search_fields = ['name', 'email', 'mobile', 'area']
    fields = ['area', 'name','mobile','email', 'cnic', 'balance']
    readonly_fields = ['balance', 'created_at', 'updated_at', 'created_by', 'updated_by']
    autocomplete_fields = ['area']


class SubscriptionAdmin(AbstractAdmin):
    list_display = ['__str__', 'price', 'connection_charges']
    search_fields = ['__str__']
    readonly_fields = ['expiry_date', 'created_at', 'updated_at', 'created_by', 'updated_by']


class PaymentAdmin(AbstractAdmin):
    list_display = ['__str__', 'price_charged']
    search_fields = ['subscription']
    readonly_fields = ['renewal_start_date', 'renewal_end_date', 'price_charged', 'created_at', 'updated_at', 'created_by', 'updated_by']
    autocomplete_fields = ['subscription']

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        res = super(PaymentAdmin, self).render_change_form(request, context, add, change, form_url, obj)
        return res

        # return TemplateResponse(request, form_template or [
        #     "admin/%s/%s/change_form.html" % (app_label, opts.model_name),
        #     "admin/%s/change_form.html" % app_label,
        #     "admin/change_form.html"
        # ], context)

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
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Payment, PaymentAdmin)
