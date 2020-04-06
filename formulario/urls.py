from django.urls import path
#from . import views
from .views import  DetalleOrdenListView_aprobador, enviarView, DetalleOrdenUpdate, DetalleOrdenListView, DetalleOrdenDelete, ClienteListView


formulario_patterns = ([
    path('', DetalleOrdenListView.as_view(), name="View_DetalleOrden"),
    path('create/<int:pk>/', enviarView.as_view(), name="createFormDetalleOrden"),
    path('selectClient', ClienteListView.as_view(), name="selectClientFormDetalleOrden"),
    path('update/<int:pk>/', DetalleOrdenUpdate.as_view(), name="update_DetalleOrden"),

    path('delete/<int:pk>/', DetalleOrdenDelete.as_view(), name="Delete_DetalleOrden"),
    #path('enviar', enviarView.as_view(), name="enviarDetalleOrden"),
    path('lista_aprobador', DetalleOrdenListView_aprobador.as_view(), name="View_DetalleOrden_aprobador"),
],'formUrl')