from django.shortcuts import render, redirect, get_object_or_404

from .models import Local, Stock,Producto
from .forms import productoForm

# Create your views here.

# def "nombre de direccion"(tipo request):
#   return render(requet, "direccion de la carpeta")
def home(request):
    return render(request, 'app/home.html')
def agregar(request):

    data = {
        'form':productoForm()
    }

    if request.method =='POST':
        formulario = productoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"]="guardado correctamente"
        else:
            data["form"]=formulario

    return render (request, 'crud/agregar.html', data)


#lista pero de la otra forma
def lista2(request):

    productos=Producto.objects.all()
    data = {
        'productos': productos
    }
    return render (request, 'crud/lista2.html',data)

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

#modificar
def modificar(request, stock_id):

    producto= get_object_or_404(Stock, id=stock_id)

    data = {
        'form': productoForm(instance=producto)
    }

    if request.method =='POST':
        formulario = productoForm(data=request.POST, instance=producto,files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="sucursales_y_stock")
        data["form"] = formulario

    return render(request, 'crud/modificar',data)

#eliminar
def eliminar_producto (request,id_producto):
    producto = get_object_or_404(Producto,pk=id_producto)
    producto.delete()
    return redirect(to="sucursales_y_stock")

def shoppingcart (request):
    return render (request, 'app/shoppingcart.html')