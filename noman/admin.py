from django.contrib import admin
from .models import Area, Package, PackageType, Client, Payment

# Register your models here.
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_at')
    search_fields = ['name']
    exclude = ['created_at',]

class PackageTypeAdmin(admin.ModelAdmin):
    list_display= ('name',)

class PackageAdmin(admin.ModelAdmin):
    list_display= ('name','status','package_type',)

class ClientAdmin(admin.ModelAdmin):
    list_display = ('name','father_name','mobile','email','cnic','price', 'status', 'created_at')
    search_fields = ['name']


admin.site.register(Area, AreaAdmin)
admin.site.register(PackageType,PackageTypeAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(Payment)
admin.site.register(Client, ClientAdmin)
