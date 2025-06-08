import requests
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RegistroUsuarioForm
from django.contrib import messages

from .models import Local, Stock,Producto
from .forms import ProductoForm, LoginForm

def home(request):
    print("SESIÓN ACTUAL:", dict(request.session))
    return render(request, 'app/home.html')

def lista2(request):
    stocks = Stock.objects.select_related('producto', 'local').all()
    return render(request, 'crud/lista2.html', {'stocks': stocks})

def sucursales_y_stock(request):
    # Usamos prefetch_related con el related_name correcto: "stocks"
    locales = Local.objects.prefetch_related('stocks__producto').all()
    return render(request, 'crud/lista.html', {'locales': locales})

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

#REISTRO USUARIO
API_URL = "http://localhost:5000/registro"  # o IP pública si está desplegado

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            try:
                response = requests.post(API_URL, json=datos)
                if response.status_code == 201:
                    messages.success(request, 'Usuario registrado exitosamente.')
                    return redirect('/')  
                else:
                    error = response.json().get('error', 'Error desconocido')
                    messages.error(request, f'Error al registrar: {error}')
            except requests.exceptions.RequestException as e:
                messages.error(request, f'Error de conexión: {str(e)}')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'sesiones/registro.html', {'form': form})


#LOGIN DEL USUARIO
def login_usuario(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            try:
                response = requests.post("http://127.0.0.1:5000/login", json=datos)
                print("RESPUESTA DE API:", response.status_code, response.text)  # <--- DEBUG

                if response.status_code == 200:
                    usuario = response.json()
                    print("USUARIO RECIBIDO:", usuario)  # <--- DEBUG

                    request.session['rut'] = usuario['rut']
                    request.session['nombre'] = usuario['nombre']
                    request.session['apellido'] = usuario['apellido']
                    request.session['tipo_usuario'] = usuario['tipo_usuario']

                    print("SESION DESPUES DE LOGIN:", dict(request.session))  # <--- DEBUG
                    
                    messages.success(request, 'Inicio de sesión exitoso.')
                    return redirect('/')  # Cambia por la ruta que desees
                else:
                    error = response.json().get('error', 'Credenciales incorrectas')
                    messages.error(request, f'Error: {error}')
            except requests.exceptions.RequestException as e:
                messages.error(request, f'Error de conexión: {str(e)}')
    else:
        form = LoginForm()
    return render(request, 'sesiones/login.html', {'form': form})

#CIERRE SESION USUARIO
def logout_usuario(request):
    request.session.flush()  # elimina toda la sesión
    return redirect('home')  # cambia a la URL que tú uses´

# Agregar producto al carrito
def agregar_al_carrito(request, producto_id):
    rut = request.session.get('rut')
    tipo_cliente = 'b2c'  # puedes cambiar según el tipo si lo guardas también
    local_id = 1  # aquí puedes mejorar con lógica futura

    if not rut:
        messages.error(request, "Debes iniciar sesión para agregar productos.")
        return redirect('login')

    # Verificar si ya existe carrito o crearlo
    try:
        # Crear o reutilizar carrito
        resp = requests.post("http://127.0.0.1:5000/carrito/crear", json={
            "usuario_rut": rut,
            "tipo_cliente": tipo_cliente
        })
        resp_data = resp.json()
        carrito_id = resp_data.get("id_carrito")

        # Agregar el producto al carrito
        resp2 = requests.post(f"http://127.0.0.1:5000/carrito/{carrito_id}/agregar_producto", json={
            "producto_id": producto_id,
            "cantidad": 1,
            "local_id": local_id
        })

        if resp2.status_code == 200:
            messages.success(request, "Producto agregado al carrito.")
        else:
            messages.error(request, resp2.json().get("error", "Error al agregar producto."))

    except requests.exceptions.RequestException as e:
        messages.error(request, f"Error de conexión con la API: {str(e)}")

    return redirect('shoppingcart')




def ver_carrito(request):
    rut = request.session.get('rut')
    if not rut:
        return redirect('login')

    # Obtener el último carrito abierto
    try:
        resp = requests.post("http://127.0.0.1:5000/carrito/crear", json={
            "usuario_rut": rut,
            "tipo_cliente": "b2c"
        })
        carrito_id = resp.json().get("id_carrito")

        # Obtener detalle del carrito
        resp = requests.get(f"http://127.0.0.1:5000/carrito/{carrito_id}")
        if resp.status_code == 200:
            carrito = resp.json()
        else:
            carrito = None
    except:
        carrito = None

    return render(request, 'app/shoppingcart.html', {'carrito': carrito})

from django.http import JsonResponse

def ver_sesion(request):
    return JsonResponse(dict(request.session))