from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Cliente
from .forms import ClienteForm

class ClienteListView(ListView):
    model = Cliente
    template_name = 'clientes/lista.html'
    context_object_name = 'clientes'


class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/form.html'
    success_url = reverse_lazy('clientes:lista')

    def form_valid(self, form):
        # Deixe o Django salvar UMA vez apenas
        response = super().form_valid(form)
        messages.success(self.request, 'Cliente cadastrado com sucesso!')
        return response

    def form_invalid(self, form):
        # Se já houver CPF duplicado, o ModelForm marca erro de form
        messages.error(self.request, 'Verifique os campos: CPF já cadastrado ou dados inválidos.')
        return super().form_invalid(form)


class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/form.html'
    success_url = reverse_lazy('clientes:lista')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Cliente atualizado com sucesso!')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Não foi possível atualizar. Verifique os campos.')
        return super().form_invalid(form)


class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'clientes/confirmar_exclusao.html'
    success_url = reverse_lazy('clientes:lista')

    def post(self, request, *args, **kwargs):
        messages.success(self.request, 'Cliente excluído com sucesso!')
        return super().post(request, *args, **kwargs)
