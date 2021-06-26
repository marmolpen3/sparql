from django import forms


class BuscarCantanteForm(forms.Form):
    cantante = forms.CharField(widget=forms.TextInput(attrs={'id': 'buscar-cantante', 'class': 'form-control', 'placeholder': 'Nombre o apellido del cantante'}))

    def is_valid(self):
        valid = super(BuscarCantanteForm, self).is_valid()
        return valid
