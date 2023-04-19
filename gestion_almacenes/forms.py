from django import forms
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Cliente
class FiltroProveedorForm(forms.Form):
    proveedor = forms.ChoiceField(choices=(), required=False, label='Filtrar por proveedor')

    def __init__(self, proveedores, *args, **kwargs):
        super(FiltroProveedorForm, self).__init__(*args, **kwargs)
        self.fields['proveedor'].choices = [('','----')] + [(proveedor, proveedor) for proveedor in proveedores]

class ClienteCreationForm(UserCreationForm):
    class Meta:
        model = Cliente
        fields = ('nombre_cliente', 'email', 'direccion_cliente', 'codigo_postal')
