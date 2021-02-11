from django.contrib import admin
from .models import Area, Package, PackageType

# Register your models here.
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_at')
    search_fields = ['name']
    exclude = ['created_at',]


admin.site.register(Area, AreaAdmin)
admin.site.register(PackageType)
admin.site.register(Package)