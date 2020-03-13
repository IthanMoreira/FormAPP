from django.urls import path
#from . import views
from .views import  enviarView, DetalleOrdenUpdate, DetalleOrdenListView, DetalleOrdenDetailView, DetalleOrdenCreate, DetalleOrdenDelete


formulario_patterns = ([
    path('', DetalleOrdenListView.as_view(), name="View_DetalleOrden"),
    path('<int:pk>/<slug:slug>/', DetalleOrdenDetailView.as_view(), name="formulario_DetalleOrden"),
    path('create', enviarView.as_view(), name="createFormDetalleOrden"),
    path('update/<int:pk>/', DetalleOrdenUpdate.as_view(), name="update_DetalleOrden"),

    path('delete/<int:pk>/', DetalleOrdenDelete.as_view(), name="Delete_DetalleOrden"),
    path('enviar', enviarView.as_view(), name="enviarDetalleOrden"),
],'formUrl')