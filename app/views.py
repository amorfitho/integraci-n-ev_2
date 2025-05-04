from django.shortcuts import render

# Create your views here.

# def "nombre de direccion"(tipo request):
#   return render(requet, "direccion de la carpeta")
def home(request):
    return render(request, 'app/home.html')
def agregar(request):
    return render (request, 'app/agregar.html')