from django.shortcuts import render

from .models import Local

# Create your views here.

# def "nombre de direccion"(tipo request):
#   return render(requet, "direccion de la carpeta")
def home(request):
    return render(request, 'app/home.html')
def agregar(request):
    return render (request, 'crud/agregar.html')
def lista(request):
    return render (request, 'crud/lista.html')

# Esto carga cada Local y sus Stock relacionados, incluyendo cada Producto asociado
def sucursales_y_stock(request):
    locales = Local.objects.prefetch_related('stocks__producto').all()
    return render(request, 'crud/lista.html', {'locales': locales})