from django.shortcuts import render, redirect, get_object_or_404

from .models import Local, Stock

# Create your views here.

# def "nombre de direccion"(tipo request):
#   return render(requet, "direccion de la carpeta")
def home(request):
    return render(request, 'app/home.html')
def agregar(request):
    return render (request, 'crud/agregar.html')

# Esto carga cada Local y sus Stock relacionados, incluyendo cada Producto asociado
def sucursales_y_stock(request):
    locales = Local.objects.prefetch_related('stocks__producto').all()
    return render(request, 'crud/lista.html', {'locales': locales})

def agregar_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    stock.cantidad += 1
    stock.save()
    return redirect('lista')

def rebajar_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    if stock.cantidad > 0:
        stock.cantidad -= 1
        stock.save()
    return redirect('lista')