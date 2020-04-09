from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .forms import DetalleOrdenForm, ClienteForm, ArticuloForm, DetalleArticuloFormSet, DetalleArticuloFormSet2
#from .forms import Venta_entradas
from .models import DetalleOrden, Cliente, Articulos
# Create your views here.

class DetalleOrdenListView(ListView):
    model = DetalleOrden
    
    paginate_by = 8
    def get_queryset(self):
        queryset = super(DetalleOrdenListView, self).get_queryset()
        filter = self.request.GET.get('filter')
        filterId = self.request.GET.get('filterId')
        if filter == 'Guardado':
            queryset = queryset.filter(Bandera_enviado=1)

        elif filter== 'Enviado':
            queryset = queryset.filter(Bandera_enviado=2)
        elif filter== 'Aprobado':
            queryset = queryset.filter(Bandera_enviado=3)
        elif filter== 'Pendiente con observaciones':
            queryset = queryset.filter(Bandera_enviado=4)
        elif filter== 'Rechazar':
            queryset = queryset.filter(Bandera_enviado=5)
        
        if filterId != '' and filterId!=None:
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


class DetalleOrdenUpdate(UpdateView):
    model=DetalleOrden
    form_class = DetalleOrdenForm
    template_name_suffix = '_update_form'
    success_url=reverse_lazy('formUrl:update_DetalleOrden') 
    def get_success_url(self):
        return reverse_lazy('formUrl:update_DetalleOrden', args=[self.object.id]) + '?ok'


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        #Obtenemos el formulario
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        #Obtenemos los detalles de la compra
        detalles = Articulos.objects.filter(datos=self.object).order_by('pk')
        detalles_data = []
        for detalle in detalles:
            
            d = {'articulo': detalle.articulo,
                 'cantidad': detalle.cantidad,
                 'desde': detalle.desde,
                 'hasta': detalle.hasta,
                 'valor_bruto': detalle.valor_bruto,
                 'detalle': detalle.detalle}
            detalles_data.append(d)
        #Ponemos como datos iniciales del formset el diccionario que hemos obtenido
        if self.object.Bandera_enviado == 2 or self.object.Bandera_enviado == 3 or self.object.Bandera_enviado == 5:
            detalle_compra_form_set = DetalleArticuloFormSet2(initial=detalles_data)
        elif self.object.Bandera_enviado == 1 or self.object.Bandera_enviado == 4:
            detalle_compra_form_set = DetalleArticuloFormSet(initial=detalles_data)

        #Renderizamos el formulario y el formset

        return self.render_to_response(self.get_context_data(form=form,
                                                         detalle_compra_form_set=detalle_compra_form_set))

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        detalle_form_set = DetalleArticuloFormSet(request.POST)
        print(detalle_form_set.is_valid())
        if form.is_valid() and detalle_form_set.is_valid():
            if 'Actualizar' in request.POST:
                self.object = form.save() 
                detalle_form_set.instance =self.object
                Articulos.objects.filter(datos = self.object).delete()
                detalle_form_set.save()
                #return redirect('formUrl:View_DetalleOrden')
            elif 'Enviar' in request.POST:
                self.object.Bandera_enviado = 2
                self.object.save()
                detalle_form_set.instance =self.object
                Articulos.objects.filter(datos = self.object).delete()
                detalle_form_set.save()
                #return redirect('formUrl:View_DetalleOrden')
            elif 'Aceptar' in request.POST:
                self.object.Bandera_enviado = 3
                self.object.save()
                #return redirect('formUrl:View_DetalleOrden_aprobador')
            elif 'Revisar' in request.POST:
                self.object.Bandera_enviado = 4
                self.object.save()
                #return redirect('formUrl:View_DetalleOrden_aprobador')
            elif 'Rechazar' in request.POST:
                self.object.Bandera_enviado = 5
                self.object.save()
                #return redirect('formUrl:View_DetalleOrden_aprobador')

        
        return super().post(request, *args, **kwargs)


class DetalleOrdenDelete(DeleteView):
    model=DetalleOrden
    success_url=reverse_lazy('formUrl:View_DetalleOrden')

class ClienteListView(ListView):
    model = Cliente    
    paginate_by = 8
    def get_queryset(self):
        queryset = super(ClienteListView, self).get_queryset()
        filterId = self.request.GET.get('filterId')        
        if filterId != '' and filterId!=None:
            queryset = queryset.filter(id_client=filterId)

        return queryset


class enviarView(TemplateView):
    model = Cliente
    template_name = "formulario/detalleorden_form.html"
    success_url=reverse_lazy('formUrl:View_DetalleOrden')
    #form_class= DetalleOrdenForm

    def get(self, request, *args, **kwargs):              
        self.object=None
        form = DetalleOrdenForm()
        DOrden = DetalleArticuloFormSet()
        return self.render_to_response(self.get_context_data(form=form,
                                                         detalle_compra_form_set=DOrden))

    def post(self, request, *args, **kwargs):    
        form = DetalleOrdenForm(request.POST)
        detalle_form_set = DetalleArticuloFormSet(request.POST)
        context = self.get_context_data(**kwargs)
        client=self.model.objects.get(id_client=context['pk'])
        
        if form.is_valid() and detalle_form_set.is_valid():
            if 'Guardar' in request.POST:                
                post = form.save(commit=False)
                post.client=client
                post.Bandera_enviado=1
                post.user=request.user
                post.save()
                detalle_form_set.instance = post
                detalle_form_set.save()
            if 'Enviar' in request.POST:
                post = form.save(commit=False)
                post.client=client
                post.Bandera_enviado=2
                post.save()
                detalle_form_set.instance = post
                detalle_form_set.save()
        else:
            print(form.is_valid())
            print(detalle_form_set.is_valid())            
            form = DetalleOrdenForm()
            
            
        return render(request, 'core/home.html')

