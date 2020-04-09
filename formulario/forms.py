from django import forms
from .models import DetalleOrden, Cliente, Articulos
from django.forms.models import inlineformset_factory

class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields=['id_client','name_cliente','RUT_cliente','categoria_cliente','name_contact']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['id_client'].disabled = True
        self.fields['name_cliente'].disabled = True
        self.fields['RUT_cliente'].disabled = True
        self.fields['categoria_cliente'].disabled = True
        self.fields['name_contact'].disabled = True

class DetalleOrdenForm(forms.ModelForm):

    class Meta:
        model = DetalleOrden
        fields=['solicitud','aumentoModificacion','documentoTributario','alimentacion']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and (self.instance.Bandera_enviado == 2 or self.instance.Bandera_enviado == 3 or self.instance.Bandera_enviado == 5):
            self.fields['solicitud'].disabled = True
            self.fields['aumentoModificacion'].disabled = True
            self.fields['documentoTributario'].disabled = True
            self.fields['alimentacion'].disabled = True

class ArticuloForm2(forms.ModelForm):

    class Meta:
        model = Articulos
        fields=['articulo','cantidad','detalle','valor_bruto','desde','hasta']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['articulo'].disabled = True
        self.fields['cantidad'].disabled = True
        self.fields['detalle'].disabled = True
        self.fields['valor_bruto'].disabled = True
        self.fields['desde'].disabled = True
        self.fields['hasta'].disabled = True

class ArticuloForm(forms.ModelForm):

    class Meta:
        model = Articulos
        fields=['articulo','cantidad','detalle','valor_bruto','desde','hasta']


DetalleArticuloFormSet = inlineformset_factory(DetalleOrden, Articulos, form= ArticuloForm, extra=5)
DetalleArticuloFormSet2 = inlineformset_factory(DetalleOrden, Articulos, form= ArticuloForm2, extra=5)
