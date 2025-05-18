from django.contrib import admin
from .models import Producto, Proveedor, FamiliaProducto, Local

# Register your models here.

class ProdctoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "familia", "precio_minorista", "precio_mayorista"]
    list_filter = ["familia", "precio_minorista"]



admin.site.register(Producto, ProdctoAdmin)
admin.site.register(Proveedor)
admin.site.register(FamiliaProducto)
admin.site.register(Local)
