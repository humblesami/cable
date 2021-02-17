from datetime import datetime

from django.contrib import admin
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from .models import Area, Package, PackageType, Client, Subscription, Payment


class ParentModelAdmin(admin.ModelAdmin):

    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',  # jquery
        )

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        try:
            res = super().changeform_view(request, object_id, form_url, extra_context)
            return res
        except Exception as e:
            return HttpResponseRedirect(request.path)

    def changelist_view(self, request, extra_context=""):
        response = super().changelist_view(request, extra_context)
        group_id = request.GET.get('group_id', None)
        if group_id:
            extra_context = {
                'group_id': group_id,
            }
            response.context_data.update(extra_context)
        #response = TemplateResponse(request, "admin/noman/change_list.html", response.context_data)
        return response

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        if obj.pk:
            obj.updated_by_id = obj.user.id
            obj.updated_at = datetime.now()
        else:
            obj.created_by_id = obj.user.id
            obj.created_at = datetime.now()
        super().save_model(request, obj, form, change)


class AreaAdmin(ParentModelAdmin):
    list_display = ['name', 'status', 'created_at']
    search_fields = ['name']
    list_filter = ['status']

    def get_queryset(self, request):
        qs = Area.full.all()
        return qs


class PackageTypeAdmin(ParentModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class PackageAdmin(ParentModelAdmin):
    list_display= ['name', 'package_type']
    search_fields = ['name', 'package_type']
    list_filter = ['package_type']
    autocomplete_fields = ['package_type']


class ClientAdmin(ParentModelAdmin):
    list_display = ['area', 'name','mobile','email', 'balance']
    search_fields = ['name', 'email', 'mobile', 'area']
    fields = ['area', 'name','mobile','email', 'cnic', 'balance']
    readonly_fields = ['balance', 'created_at', 'updated_at', 'created_by', 'updated_by']
    autocomplete_fields = ['area']


class SubscriptionAdmin(ParentModelAdmin):
    list_display = ['__str__', 'price', 'connection_charges']
    search_fields = ['__str__']
    readonly_fields = ['expiry_date', 'created_at', 'updated_at', 'created_by', 'updated_by']

    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',
            '/static/change_form_subscription.js',
        )


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        exclude = []

    def save(self, commit=True):
        # Save the provided password in hashed format
        obj = super().save(commit=False)
        if commit:
            obj.save()
        return obj

    def clean(self):
        super().clean()
        due_amount = self.cleaned_data.get('due_amount')
        being_paid = self.cleaned_data.get('amount')

        if not being_paid:
            being_paid = 0
        if not due_amount:
            due_amount = 0
        amount_error = 'Give amount must be non zero'# and at least half of due amount='+str(due_amount)
        valid_amount = being_paid and being_paid > 0
        #valid_amount = being_paid and being_paid < due_amount / 2
        if not valid_amount:
            self._errors['amount'] = self.error_class([amount_error])
        return self.cleaned_data


class PaymentAdmin(ParentModelAdmin):
    form = PaymentForm
    add_form = PaymentForm

    list_display = ['__str__', 'due_amount']
    search_fields = ['subscription']
    readonly_fields = ['renewal_start_date', 'renewal_end_date', 'created_at', 'updated_at', 'created_by', 'updated_by']
    autocomplete_fields = ['subscription']

    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',
            '/static/change_form_payment.js',
        )
        css = {
            'all': ('/static/payment.css ',)
        }

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


admin.site.register(Area, AreaAdmin)
admin.site.register(PackageType,PackageTypeAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Payment, PaymentAdmin)
