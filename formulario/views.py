from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .forms import DetalleOrdenForm
#from .forms import Venta_entradas
from .models import DetalleOrden
# Create your views here.

class DetalleOrdenListView(ListView):
    model = DetalleOrden
    
    paginate_by = 8
    def get_queryset(self):
        queryset = super(DetalleOrdenListView, self).get_queryset()
        filter = self.request.GET.get('filter')
        filterId = self.request.GET.get('filterId')
        print(type(filterId))
        if filter == 'Guardado':
            queryset = queryset.filter(Bandera_enviado=1)

        elif filter== 'Enviado':
            queryset = queryset.filter(Bandera_enviado=2)
        elif filter== 'Aprobado':
            queryset = queryset.filter(Bandera_enviado=3)
        elif filter== 'Pendiente con observaciones':
            queryset = queryset.filter(Bandera_enviado=4)
        
        if filterId != '' and filterId!=None:
            print(filterId)
            queryset = queryset.filter(id=filterId)

        return queryset



class DetalleOrdenListView_aprobador(ListView):
    model = DetalleOrden
    template_name = "formulario/detalleorden_list_aprobador.html"
    paginate_by = 5
    def get_queryset(self):
        queryset = super(DetalleOrdenListView_aprobador, self).get_queryset()
        filterId = self.request.GET.get('filterId')
        queryset = queryset.filter(Bandera_enviado=2)
        if filterId != '' and filterId!=None:
            print(filterId)
            queryset = queryset.filter(id=filterId)
        return queryset


class DetalleOrdenDetailView(DetailView):
    model = DetalleOrden

class DetalleOrdenCreate(CreateView):
    model=DetalleOrden
    fields=['client','contacto','solicitud','aumentoModificacion','documentoTributario','alimentacion']
    success_url=reverse_lazy('formUrl:enviarDetalleOrden')


class DetalleOrdenUpdate(UpdateView):
    model=DetalleOrden
    form_class = DetalleOrdenForm
    template_name_suffix = '_update_form'
    success_url=reverse_lazy('formUrl:update_DetalleOrden') 
    def get_success_url(self):
        return reverse_lazy('formUrl:update_DetalleOrden', args=[self.object.id]) + '?ok'


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'Enviar' in request.POST:
            self.object.Bandera_enviado = 2
            self.object.save()
            return redirect('formUrl:View_DetalleOrden')
        if 'Aceptar' in request.POST:
            self.object.Bandera_enviado = 3
            self.object.save()
            return redirect('formUrl:View_DetalleOrden_aprobador')
        if 'Rechazar' in request.POST:
            self.object.Bandera_enviado = 4
            self.object.save()
            return redirect('formUrl:View_DetalleOrden_aprobador')
        return super().post(request, *args, **kwargs)


class DetalleOrdenDelete(DeleteView):
    model=DetalleOrden
    success_url=reverse_lazy('formUrl:View_DetalleOrden')


class enviarView(TemplateView):
    
    template_name = "formulario/detalleorden_form.html"

    def get(self, request, *args, **kwargs):
        form = DetalleOrdenForm()
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):    
        form = DetalleOrdenForm(request.POST)
        if form.is_valid():
            if 'Guardar' in request.POST:
                post = form.save(commit=False)
                post.Bandera_enviado=1
                post.save()

            if 'Enviar' in request.POST:
                post = form.save(commit=False)
                post.Bandera_enviado=2
                post.save()

        else:
            form = DetalleOrdenForm()
            
            
        return render(request, "core/base.html",{'form':DetalleOrden})

