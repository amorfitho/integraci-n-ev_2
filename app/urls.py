from django.urls import path
from.views import home, agregar, lista, sucursales_y_stock

# importar nombre puesto en def de la pagian desde "views"
#   path('nombre de la pagina/', nombre_de_la_pagina, name= nombre de la pagina(esto es para el direcionamiento con botones))

urlpatterns = [
    path('', home, name="home"),
    path('agregar/',agregar,name="agregar"),
    path('lista/', sucursales_y_stock, name="lista"),
]