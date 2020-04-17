from django.urls import path
#from . import views
from .views import  AGGCommentUpdate, DetalleOrdenListView_tesoreria, DetalleOrdenListView_aprobador, enviarView, DetalleOrdenUpdate, DetalleOrdenListView, DetalleOrdenDelete, ClienteListView


formulario_patterns = ([
    path('', DetalleOrdenListView.as_view(), name="View_DetalleOrden"),
    path('create/<int:pk>/', enviarView.as_view(), name="createFormDetalleOrden"),
    path('selectClient', ClienteListView.as_view(), name="selectClientFormDetalleOrden"),
    path('update/<int:pk>/', DetalleOrdenUpdate.as_view(), name="update_DetalleOrden"),
    path('comment/<int:pk>/', AGGCommentUpdate.as_view(), name="update_comentario"), 
    path('delete/<int:pk>/', DetalleOrdenDelete.as_view(), name="Delete_DetalleOrden"),
    path('lista_tesoreria', DetalleOrdenListView_tesoreria.as_view(), name="View_DetalleOrden_tesoreria"),
    path('lista_aprobador', DetalleOrdenListView_aprobador.as_view(), name="View_DetalleOrden_aprobador"),
],'formUrl')

