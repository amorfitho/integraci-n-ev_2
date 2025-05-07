from django.urls import path
from.views import home, agregar, sucursales_y_stock, agregar_stock, rebajar_stock

# importar nombre puesto en def de la pagian desde "views"
#   path('nombre de la pagina/', nombre_de_la_pagina, name= nombre de la pagina(esto es para el direcionamiento con botones))

urlpatterns = [
    path('', home, name="home"),
    path('agregar/',agregar,name="agregar"),
    path('lista/', sucursales_y_stock, name="lista"),
    path('stock/agregar/<int:stock_id>/', agregar_stock, name='agregar_stock'),
    path('stock/rebajar/<int:stock_id>/', rebajar_stock, name='rebajar_stock'),
]