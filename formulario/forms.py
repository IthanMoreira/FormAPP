from django import forms
from .models import DetalleOrden

class DetalleOrdenForm(forms.ModelForm):

    class Meta:
        model = DetalleOrden
        fields=['client','contacto','solicitud','aumentoModificacion','documentoTributario','alimentacion']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.Bandera_enviado == 2:
            self.fields['client'].disabled = True
            self.fields['contacto'].disabled = True
            self.fields['solicitud'].disabled = True
            self.fields['aumentoModificacion'].disabled = True
            self.fields['documentoTributario'].disabled = True
            self.fields['alimentacion'].disabled = True