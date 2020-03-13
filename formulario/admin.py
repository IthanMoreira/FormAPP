from django.contrib import admin
from .models import Direccion, Cliente, Contacto, DetalleOrden

# Register your models here.
#admin.site.register(Vendedores)


#admin.site.register(Venta)

admin.site.register(Direccion)
admin.site.register(Cliente)
admin.site.register(Contacto)
admin.site.register(DetalleOrden)


