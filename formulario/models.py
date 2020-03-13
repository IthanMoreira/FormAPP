from django.db import models
from django.contrib.auth.models import User
from django.dispatch import Signal

from django.contrib.auth import get_user_model

class Direccion (models.Model):
    direccion= models.CharField(max_length=100, verbose_name="Dirección",default='null')
    comuna= models.CharField(max_length=100, verbose_name="Comuna",default='null')
    ciudad= models.CharField(max_length=100, verbose_name="Ciudad",default='null')   
    provincia=models.CharField(max_length=100, verbose_name="Provincia",default='null')   
    zip_code=models.CharField(max_length=100, verbose_name="ZIP Code",default='null')   
    pais=models.CharField(max_length=100, verbose_name="País",default='null')   

    def __str__(self):
        return self.direccion

class Cliente (models.Model):
    name_cliente= models.CharField(max_length=100, verbose_name="Nombre del Cliente")
    RUT_cliente= models.CharField(max_length=100, verbose_name="RUT del Cliente")
    categoria_cliente= models.CharField(max_length=100, verbose_name="Categoria de Cliente")
    direccion=models.ForeignKey(Direccion,on_delete=models.PROTECT)
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.name_cliente



class Contacto(models.Model):
    registro_contacto= models.CharField(max_length=100, verbose_name="Registro de Contacto en Sistema")
    nombreApellido= models.CharField(max_length=100, verbose_name="Nombre y Apellido Contacto")
    tipo_contacto= models.CharField(max_length=100, verbose_name="RUT del Cliente")

    def __str__(self):
        return self.registro_contacto
   

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
)  

class DetalleOrden(models.Model):
    client=models.ForeignKey(Cliente, on_delete=models.PROTECT)
    contacto=models.ForeignKey(Contacto, on_delete=models.PROTECT)
    solicitud= models.CharField(default='NUEVA ORDEN',choices=solicitud_CHOICE,max_length=100, verbose_name="Tipo de Solicitud")
    aumentoModificacion= models.CharField(max_length=100, verbose_name="En caso de aumento o modificación ingrese el  N° DE ORDEN",blank=True,null=True)
    documentoTributario= models.CharField(max_length=30,choices=DEMO_CHOICES,default='Factura' ,verbose_name="Documento Tributario")
    alimentacion= models.CharField(default='NO',choices=alimentacion_CHOICES,max_length=100, verbose_name="Incluye Alimentación")
    Bandera_enviado=models.IntegerField(choices=estado_orden_CHOICE,default=1,verbose_name="Enviado")
    class Meta:
        verbose_name = "DetalleOrden"
        verbose_name_plural = "DetalleOrdenes"

    def __str__(self):
        return self.solicitud




