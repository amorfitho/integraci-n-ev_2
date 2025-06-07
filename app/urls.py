from django.urls import path
from.views import home, agregar,lista2 ,sucursales_y_stock, rebajar_stock, modificar, eliminar_producto, shoppingcart, modificar, eliminar_stock, registro_usuario, login_usuario, logout_usuario, agregar_al_carrito, ver_carrito

# importar nombre puesto en def de la pagian desde "views"
#   path('nombre de la pagina/', nombre_de_la_pagina, name= nombre de la pagina(esto es para el direcionamiento con botones))

urlpatterns = [
    path('', home, name="home"),
    path('agregar/',agregar,name="agregar"),
    path('lista/', sucursales_y_stock, name="lista"),
    path('lista2/', lista2, name="lista2"),
    path('modificar/<int:stock_id>/', modificar, name='modificar'),
    path('stock/agregar/<int:stock_id>/', agregar, name='agregar_stock'),
    path('stock/rebajar/<int:stock_id>/', rebajar_stock, name='rebajar_stock'),
    path('eliminar_producto/<int:id_producto>/',eliminar_producto, name='eliminar_producto'),
    path('shoppingcart/', shoppingcart, name="shoppingcart"),
    path('eliminar/<int:stock_id>/', eliminar_stock, name='eliminar'),
    path('registro/', registro_usuario, name='registro'),
    path('login/', login_usuario, name='login'),
    path('logout/', logout_usuario, name='logout'),
    path('shoppingcart/agregar/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('shoppingcart/', ver_carrito, name='shoppingcart')
]