from django.db import models

# Create your models here.

class FamiliaProducto(models.Model):
    id_familia = models.AutoField(primary_key=True)
    nombre_familia = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_familia
    
class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre_proveedor=models.CharField(max_length=80)
    descripcion = models.TextField(blank=True)
    telefono_proveedor=models.CharField(max_length=80)
    direccion_proveedor=models.CharField(max_length=120)

    def __str__(self):
        return self.nombre_proveedor


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    familia = models.ForeignKey(FamiliaProducto, on_delete=models.CASCADE, related_name='productos')
    nombre = models.CharField(max_length=150)
    precio = models.IntegerField()
    descripcion = models.TextField(blank=True)
    fecha_fabricacion = models.DateField(null=True, blank=True)
    imagen = models.ImageField(upload_to="productos", null=True)

    def __str__(self):
        return self.nombre
    
class TipoUsuario(models.Model):
    nombre_tipo_usuario = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_tipo_usuario

class Usuario(models.Model):
    rut = models.CharField(max_length=8, primary_key=True)  # sin dígito verificador
    nombre_usuario = models.CharField(max_length=50)
    apellido_usuario = models.CharField(max_length=50)
    contrasena = models.CharField(max_length=128)
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nombre_usuario} {self.apellido_usuario} ({self.rut})'
    
# Modelo de Local
class Local(models.Model):
    id_local = models.AutoField(primary_key=True)
    nombre_local = models.CharField(max_length=150)
    direccion = models.CharField(max_length=255)
    # Se pueden agregar más atributos dependiendo de lo que se necesite, como ubicación geográfica, teléfono, etc.

    def __str__(self):
        return self.nombre_local


# Modelo de Stock de Producto en Local
class Stock(models.Model):
    local = models.ForeignKey(Local, on_delete=models.CASCADE, related_name='stocks')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='stocks')
    cantidad = models.PositiveIntegerField(default=0)  # Cantidad disponible de este producto en el local

    class Meta:
        unique_together = ('local', 'producto')  # Evitar duplicados, asegurando que no haya dos entradas para el mismo producto en un mismo local

    def __str__(self):
        return f'{self.producto.nombre} - {self.local.nombre_local} - {self.cantidad} disponibles'

