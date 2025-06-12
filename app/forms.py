from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):


    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            "fecha_fabricacion": forms.SelectDateWidget(empty_label=("Seleccione Año", "Seleccione Mes", "Seleccione Día")),
        }

class RegistroUsuarioForm(forms.Form):
    rut = forms.CharField(max_length=12, label="RUT")
    nombre = forms.CharField(max_length=100)
    apellido = forms.CharField(max_length=100)
    contrasena = forms.CharField(widget=forms.PasswordInput)
    tipo_usuario = forms.ChoiceField(choices=[
        (1, 'Cliente B2B'),
        (2, 'Cliente B2C'),
        (3, 'Bodeguero'),
        (4, 'Vendedor'),
        (5, 'Administrador')
    ])
    direccion = forms.CharField(required=False)

class LoginForm(forms.Form):
    rut = forms.CharField(
        label='RUT',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu RUT'
        })
    )
    contrasena = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu contraseña'
        })
    )