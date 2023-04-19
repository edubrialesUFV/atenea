from django import forms

class FiltroProveedorForm(forms.Form):
    proveedor = forms.ChoiceField(choices=(), required=False, label='Filtrar por proveedor')

    def __init__(self, proveedores, *args, **kwargs):
        super(FiltroProveedorForm, self).__init__(*args, **kwargs)
        self.fields['proveedor'].choices = [('','----')] + [(proveedor, proveedor) for proveedor in proveedores]

