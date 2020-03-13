from django import forms
from .models import DetalleOrden

class DetalleOrdenForm(forms.ModelForm):

    class Meta:
        model = DetalleOrden
        fields=['client','contacto','solicitud','aumentoModificacion','documentoTributario','alimentacion']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.Bandera_enviado:
            self.fields['client'].widget.attrs.update({'disabled': True})
            self.fields['contacto'].widget.attrs.update({'disabled': True})
            self.fields['solicitud'].widget.attrs.update({'disabled': True})
            self.fields['aumentoModificacion'].widget.attrs.update({'disabled': True})
            self.fields['documentoTributario'].widget.attrs.update({'disabled': True})
            self.fields['alimentacion'].widget.attrs.update({'disabled': True})