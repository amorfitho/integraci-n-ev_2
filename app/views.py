from django.shortcuts import render, redirect, get_object_or_404

from .models import Local, Stock,Producto
from .forms import ProductoForm

def home(request):
    return render(request, 'app/home.html')

def lista2(request):
    stocks = Stock.objects.select_related('producto', 'local').all()
    return render(request, 'crud/lista2.html', {'stocks': stocks})

def sucursales_y_stock(request):
    locales = Local.objects.prefetch_related('stocks__producto').all()
    stocks = Stock.objects.select_related('producto', 'local').all()
    return render(request, 'crud/lista.html', {'stocks': stocks})

def agregar(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save()
            local_default = Local.objects.first()
            if local_default:
                Stock.objects.create(local=local_default, producto=producto, cantidad=0)
            return redirect('lista2')
    else:
        form = ProductoForm()
    return render(request, 'crud/agregar.html', {'form': form})



def rebajar_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    if stock.cantidad > 0:
        stock.cantidad -= 1
        stock.save()
    return redirect('lista')

#modificar
def modificar(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    producto = stock.producto  

    if request.method == 'POST':
        formulario = ProductoForm(request.POST, request.FILES, instance=producto)
        if formulario.is_valid():
            formulario.save()
            return redirect('lista2')
    else:
        formulario = ProductoForm(instance=producto)

    return render(request, 'crud/modificar.html', {'form': formulario})

#eliminar
def eliminar_producto (request,id_producto):
    producto = get_object_or_404(Producto,pk=id_producto)
    producto.delete()
    messages.success(request, 'Producto eliminado correctamente.')
    return redirect('lista')

def shoppingcart (request):
    return render (request, 'app/shoppingcart.html')

def eliminar_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    stock.delete()
    return redirect('lista')

