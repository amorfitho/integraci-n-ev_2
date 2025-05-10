from django.contrib import admin
from .models import Producto, Proveedor, FamiliaProducto, Local

# Register your models here.

class ProdctoAdmin(admin.ModelAdmin):
    list_display = ["nombre","familia","precio"]
    list_filter =["familia","precio"] 



admin.site.register(Producto, ProdctoAdmin)
admin.site.register(Proveedor)
admin.site.register(FamiliaProducto)
admin.site.register(Local)
