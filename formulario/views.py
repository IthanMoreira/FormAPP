from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .forms import DetalleOrdenForm_comment, DetalleOrdenForm, ClienteForm, ArticuloForm, DetalleArticuloFormSet, DetalleArticuloFormSet2
#from .forms import Venta_entradas
from .models import DetalleOrden, Cliente, Articulos, User
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
        elif filter== 'AprobadoTesoreria':
            queryset = queryset.filter(Bandera_enviado=6)
        elif filter== 'POTesoreria':
            queryset = queryset.filter(Bandera_enviado=7)
        elif filter== 'RechazarTesorería':
            queryset = queryset.filter(Bandera_enviado=8)
        if filterId != '' and filterId!=None:
            queryset = queryset.filter(created=filterId)
            
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
            queryset = queryset.filter(created=filterId)
        return queryset

class DetalleOrdenListView_tesoreria(ListView):
    model = DetalleOrden
    template_name = "formulario/detalleorden_list_tesoreria.html"
    paginate_by = 5
    def get_queryset(self):
        queryset = super(DetalleOrdenListView_tesoreria, self).get_queryset()
        filterId = self.request.GET.get('filterId')
        queryset = queryset.filter(Bandera_enviado=3)
        if filterId != '' and filterId!=None:            
            queryset = queryset.filter(created=filterId)

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
        #Obtenemos el comentario si lo tiene
        
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
        if self.object.Bandera_enviado == 2 or self.object.Bandera_enviado == 3 or self.object.Bandera_enviado == 5 or self.object.Bandera_enviado == 6:
            detalle_compra_form_set = DetalleArticuloFormSet2(initial=detalles_data)
        elif self.object.Bandera_enviado == 1 or self.object.Bandera_enviado == 4:
            detalle_compra_form_set = DetalleArticuloFormSet(initial=detalles_data)

        #Renderizamos el formulario y el formset

        return self.render_to_response(self.get_context_data(form=form,
            detalle_compra_form_set=detalle_compra_form_set,comment=self.object.coment_ecomer))

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        detalle_form_set = DetalleArticuloFormSet(request.POST)
        
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
                return redirect('formUrl:View_DetalleOrden_aprobador')
            elif 'Revisar' in request.POST:
                return redirect('formUrl:update_comentario', pk=self.object.id)
            elif 'Rechazar' in request.POST:
                self.object.Bandera_enviado = 5
                self.object.save()
                return redirect('formUrl:View_DetalleOrden_tesoreria')
            elif 'Aceptar_tesoreria' in request.POST:
                self.object.Bandera_enviado = 6
                self.object.save()
                return redirect('formUrl:View_DetalleOrden_tesoreria')
            elif 'Revisar_tesoreria' in request.POST:
                return redirect('formUrl:update_comentario', pk=self.object.id)
            elif 'Rechazar_tesoreria' in request.POST:
                self.object.Bandera_enviado = 8
                self.object.save()
                return redirect('formUrl:View_DetalleOrden_tesoreria')
        
        return super().post(request, *args, **kwargs)


class AGGCommentUpdate(UpdateView):
    model=DetalleOrden
    template_name = "formulario/detalleorden_confirm_comment.html"
    success_url=reverse_lazy('formUrl:update_comentario') 
    def get_success_url(self):
        return reverse_lazy('formUrl:update_comentario', args=[self.object.id]) + '?ok'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        #Obtenemos el formulario
        form = DetalleOrdenForm_comment
        #Renderizamos el formulario y el formset
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        form=DetalleOrdenForm_comment
        if request.method == "POST":
            form = DetalleOrdenForm_comment(request.POST)                      
            if form.is_valid():
                if 'SiEnviarApro' in request.POST:
                    #sirve mucho para unificar
                    #print(request.user.groups.all().values().get()['name'])


                    self.object.coment_ecomer=request.POST.get('comentario','')
                    self.object.Bandera_enviado = 4
                    self.object.save()
                    #return redirect('formUrl:update_comentario', pk=self.object.id)
                elif 'SiEnviarTeso' in request.POST:
                    self.object.coment_ecomer=request.POST.get('comentario','')
                    self.object.Bandera_enviado = 7
                    self.object.save()
                    #return redirect('formUrl:update_comentario', pk=self.object.id)
        
        return render(request, 'core/home.html')




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
                post.user=request.user
                post.save()
                detalle_form_set.instance = post
                detalle_form_set.save()
        else:
            form = DetalleOrdenForm()
            
            
        return render(request, 'core/home.html')

