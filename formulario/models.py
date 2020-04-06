from django.db import models
from django.contrib.auth.models import User
from django.dispatch import Signal

from django.contrib.auth import get_user_model


class Cliente (models.Model):
    id_client=models.CharField(max_length=100, verbose_name="Id del cliente",primary_key=True)
    name_cliente= models.CharField(max_length=100, verbose_name="Nombre del Cliente")
    RUT_cliente= models.CharField(max_length=100, verbose_name="RUT del Cliente")
    categoria_cliente= models.CharField(max_length=100, verbose_name="Categoria de Cliente")
    name_contact=models.CharField(max_length=100, verbose_name="Nombre contacto")
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering=['name_cliente']
        
    def __str__(self):
        return self.id_client

DEMO_CHOICES = ( 
    ("Boleta", "Boleta"), 
    ("Factura", "Factura"), 
)  
#derecha se muestra
alimentacion_CHOICES = ( 
    ("SI", "SI"), 
    ("NO", "NO"), 
)  
solicitud_CHOICE = ( 
    ("NUEVA ORDEN", "NUEVA ORDEN"), 
    ("AUMENTO DE ORDEN", "AUMENTO DE ORDEN"), 
    ("MODIFICACION DE ORDEN", "MODIFICACION DE ORDEN"), 
)
estado_orden_CHOICE = ( 
    (1, "Guardado"), 
    (2, "Enviado"), 
    (3, "Aprobado"),
    (4, "Pendiente con observaciones"),
    (5, "Rechazar"),
)  

class DetalleOrden(models.Model):
    client=models.ForeignKey(Cliente, on_delete=models.PROTECT,verbose_name="Cliente")
    solicitud= models.CharField(default='NUEVA ORDEN',choices=solicitud_CHOICE,max_length=100, verbose_name="Tipo de Solicitud")
    aumentoModificacion= models.CharField(max_length=100, verbose_name="En caso de aumento o modificación ingrese el  N° DE ORDEN",blank=True,null=True)
    documentoTributario= models.CharField(max_length=30,choices=DEMO_CHOICES,default='Factura' ,verbose_name="Documento Tributario")
    alimentacion= models.CharField(default='NO',choices=alimentacion_CHOICES,max_length=100, verbose_name="Incluye Alimentación")
    Bandera_enviado=models.IntegerField(choices=estado_orden_CHOICE,default=1,verbose_name="Enviado")
    class Meta:
        verbose_name = "DetalleOrden"
        verbose_name_plural = "DetalleOrdenes"
        ordering=['client']

class Articulos(models.Model):
    datos=models.ForeignKey(DetalleOrden, on_delete=models.CASCADE,verbose_name="Datos")
    articulo= models.CharField(default=' ',max_length=100, verbose_name="Articulo",blank=True,null=True)
    cantidad= models.IntegerField(default=0, verbose_name="Cantidad",blank=True,null=True)
    detalle= models.CharField(default=' ', max_length=30, verbose_name="Detalle",blank=True,null=True)
    tipo= models.CharField(default=' ', max_length=100, verbose_name="Tipo",blank=True,null=True)
    class Meta:
        verbose_name = "Articulo"
        verbose_name_plural = "Articulos"