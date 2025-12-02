from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.db.models import Sum, Avg
from .models import Pet, Scheduling, Tutor, Service, Note
from .forms import SchedulingForm
from datetime import date
from decimal import Decimal
import json

# ==================================================================================== #
# FUNÇÃO DE TESTE DE PERMISSÃO POR MODELO
# ==================================================================================== #
def has_model_permission(user, perm_name):

    return user.is_authenticated and user.has_perm(perm_name)

# ==================================================================================== #
# 1. Views do Sistema
# ==================================================================================== #
@login_required(login_url='login')
def home_view(request):
    total_pets = Pet.objects.count()
    total_agendamentos = Scheduling.objects.filter(status='Não').count()
    context = {'total_pets': total_pets, 'total_agendamentos': total_agendamentos}
    return render(request, 'home.html', context)

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='login')
def dashboard_view(request):
    todos_agendamentos = Scheduling.objects.all()
    agendamentos_pagos = todos_agendamentos.filter(status='Sim')
    agendamentos_pendentes = todos_agendamentos.filter(status='Não')

    total_pets = Pet.objects.count()
    total_tutors = Tutor.objects.count()
    count_pendentes = agendamentos_pendentes.count()

    soma_total_pago = agendamentos_pagos.aggregate(Sum('total_value'))['total_value__sum'] or Decimal('0.00')
    soma_total_pendente = agendamentos_pendentes.aggregate(Sum('total_value'))['total_value__sum'] or Decimal('0.00')

    ticket_medio = todos_agendamentos.aggregate(Avg('total_value'))['total_value__avg']
    ticket_medio = round(ticket_medio, 2) if ticket_medio else Decimal('0.00')

    proximos_agendamentos = todos_agendamentos.filter(date_scheduling__gte=date.today()).order_by('date_scheduling')[:5]
    count_pagos = agendamentos_pagos.count()

    chart_data = {'labels': ['Pagos', 'Pendentes'],
                'data': [int(count_pagos), int(count_pendentes)],
                'colors': ['#198754', '#dc3545']}

    context = {
        'total_pets': total_pets,
        'total_tutors': total_tutors,
        'total_agendamentos_pendentes': count_pendentes,
        'soma_total_pago': soma_total_pago,
        'soma_total_pendente': soma_total_pendente,
        'ticket_medio': ticket_medio,
        'proximos_agendamentos': proximos_agendamentos,
        'chart_data_json': json.dumps(chart_data),
    }
    return render(request, 'dashboard.html', context)

# ==================================================================================== #
# 2. Views de Pets
# ==================================================================================== #
@method_decorator(login_required, name='dispatch')
class PetCreateView(CreateView):
    model = Pet
    fields = ['name', 'species', 'race', 'age', 'sex', 'weight', 'medical_observations', 'photo', 'tutor']
    template_name = 'pet_form.html'
    success_url = reverse_lazy('pet_list')

    def dispatch(self, request, *args, **kwargs):
        if not has_model_permission(request.user, 'daycare.add_pet'):
            messages.warning(request, "Você não tem permissão para criar pets.")
            return redirect('pet_list')
        return super().dispatch(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class PetUpdateView(UpdateView):
    model = Pet
    fields = ['name', 'species', 'race', 'age', 'sex', 'weight', 'medical_observations', 'photo', 'tutor']
    template_name = 'pet_form.html'
    success_url = reverse_lazy('pet_list')

    def dispatch(self, request, *args, **kwargs):
        if not has_model_permission(request.user, 'daycare.change_pet'):
            messages.warning(request, "Você não tem permissão para editar pets.")
            return redirect('pet_list')
        return super().dispatch(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class PetDeleteView(DeleteView):
    model = Pet
    template_name = 'pet_confirm_delete.html'
    success_url = reverse_lazy('pet_list')
    context_object_name = 'pet'

    def dispatch(self, request, *args, **kwargs):
        if not has_model_permission(request.user, 'daycare.delete_pet'):
            messages.warning(request, "Você não tem permissão para excluir pets.")
            return redirect('pet_list')
        return super().dispatch(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class PetListView(ListView):
    model = Pet
    template_name = 'pet_list.html'
    context_object_name = 'pet_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_term"] = self.request.GET.get('q', '')
        return context

@method_decorator(login_required, name='dispatch')
class PetDetailView(DetailView):
    model = Pet
    template_name = 'pet_detail.html'
    context_object_name = 'pet'

# ==================================================================================== #
# 3. Views de Tutores
# ==================================================================================== #
@method_decorator(login_required, name='dispatch')
class TutorCreateView(CreateView):
    model = Tutor
    fields = ['name', 'cpf', 'phone_number', 'email', 'address', 'state', 'city', 'know']
    template_name = 'tutor_form.html'
    success_url = reverse_lazy('tutor_list')

    def dispatch(self, request, *args, **kwargs):
        if not has_model_permission(request.user, 'daycare.add_tutor'):
            messages.warning(request, "Você não tem permissão para criar tutores.")
            return redirect('tutor_list')
        return super().dispatch(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class TutorUpdateView(UpdateView):
    model = Tutor
    fields = ['name', 'cpf', 'phone_number', 'email', 'address', 'state', 'city', 'know']
    template_name = 'tutor_form.html'
    success_url = reverse_lazy('tutor_list')

    def dispatch(self, request, *args, **kwargs):
        if not has_model_permission(request.user, 'daycare.change_tutor'):
            messages.warning(request, "Você não tem permissão para editar tutores.")
            return redirect('tutor_list')
        return super().dispatch(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class TutorDeleteView(DeleteView):
    model = Tutor
    template_name = 'tutor_confirm_delete.html'
    success_url = reverse_lazy('tutor_list')
    context_object_name = 'tutor'

    def dispatch(self, request, *args, **kwargs):
        if not has_model_permission(request.user, 'daycare.delete_tutor'):
            messages.warning(request, "Você não tem permissão para excluir tutores.")
            return redirect('tutor_list')
        return super().dispatch(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class TutorListView(ListView):
    model = Tutor
    template_name = 'tutor_list.html'
    context_object_name = 'tutor_list'
    paginate_by = 15
    ordering = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_term"] = self.request.GET.get('q', '')
        return context

# ==================================================================================== #
# 4. Views de Agendamentos
# ==================================================================================== #
@method_decorator(login_required, name='dispatch')
class SchedulingCreateView(CreateView):
    model = Scheduling
    form_class = SchedulingForm
    template_name = 'scheduling_form.html'
    success_url = reverse_lazy('scheduling_list')

    def dispatch(self, request, *args, **kwargs):
        if not has_model_permission(request.user, 'daycare.add_scheduling'):
            messages.warning(request, "Você não tem permissão para criar agendamentos.")
            return redirect('scheduling_list')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        services = Service.objects.all().values('id', 'price')
        context['services_json'] = json.dumps([{'id': s['id'], 'price': str(s['price'])} for s in services])
        return context

    def form_valid(self, form):
        self.object = form.save()
        if hasattr(self.object, 'calculate_values'):
            self.object.calculate_values()
            self.object.save()
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class SchedulingUpdateView(UpdateView):
    model = Scheduling
    form_class = SchedulingForm
    template_name = 'scheduling_form.html'
    success_url = reverse_lazy('scheduling_list')

    def dispatch(self, request, *args, **kwargs):
        if not has_model_permission(request.user, 'daycare.change_scheduling'):
            messages.warning(request, "Você não tem permissão para editar agendamentos.")
            return redirect('scheduling_list')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        services = Service.objects.all().values('id', 'price')
        context['services_json'] = json.dumps([{'id': s['id'], 'price': str(s['price'])} for s in services])
        return context

@method_decorator(login_required, name='dispatch')
class SchedulingDeleteView(DeleteView):
    model = Scheduling
    template_name = 'scheduling_confirm_delete.html'
    success_url = reverse_lazy('scheduling_list')
    context_object_name = 'scheduling'

    def dispatch(self, request, *args, **kwargs):
        if not has_model_permission(request.user, 'daycare.delete_scheduling'):
            messages.warning(request, "Você não tem permissão para excluir agendamentos.")
            return redirect('scheduling_list')
        return super().dispatch(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class SchedulingListView(ListView):
    model = Scheduling
    template_name = 'scheduling_list.html'
    context_object_name = 'scheduling_list'
    ordering = ['-date_scheduling']

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        status = self.request.GET.get('status')
        if query:
            queryset = queryset.filter(tutor__name__icontains=query)
        if status in ['Sim', 'Não']:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_term"] = self.request.GET.get('q', '')
        context["selected_status"] = self.request.GET.get('status', '')
        return context

# ==================================================================================== #
# 5. Views de Serviços
# ==================================================================================== #
@method_decorator(login_required, name='dispatch')
class ServiceCreateView(CreateView):
    model = Service
    fields = ['name', 'description', 'price']
    template_name = 'service_form.html'
    success_url = reverse_lazy('service_list')

    def dispatch(self, request, *args, **kwargs):
        if not has_model_permission(request.user, 'daycare.add_service'):
            messages.warning(request, "Você não tem permissão para criar serviços.")
            return redirect('service_list')
        return super().dispatch(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class ServiceUpdateView(UpdateView):
    model = Service
    fields = ['name', 'description', 'price']
    template_name = 'service_form.html'
    success_url = reverse_lazy('service_list')

    def dispatch(self, request, *args, **kwargs):
        if not has_model_permission(request.user, 'daycare.change_service'):
            messages.warning(request, "Você não tem permissão para editar serviços.")
            return redirect('service_list')
        return super().dispatch(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class ServiceDeleteView(DeleteView):
    model = Service
    template_name = 'service_confirm_delete.html'
    success_url = reverse_lazy('service_list')
    context_object_name = 'service'

    def dispatch(self, request, *args, **kwargs):
        if not has_model_permission(request.user, 'daycare.delete_service'):
            messages.warning(request, "Você não tem permissão para excluir serviços.")
            return redirect('service_list')
        return super().dispatch(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class ServiceListView(ListView):
    model = Service
    template_name = 'service_list.html'
    context_object_name = 'service_list'
    paginate_by = 15
    ordering = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_term"] = self.request.GET.get('q', '')
        return context

# ==================================================================================== #
# 6. Nota de Serviço
# ==================================================================================== #
@login_required(login_url='login')
def generate_note_view(request, pk):
    scheduling = get_object_or_404(Scheduling, pk=pk)
    if not has_model_permission(request.user, 'daycare.add_note'):
        messages.warning(request, "Você não tem permissão para gerar notas.")
        return redirect('scheduling_list')
    if hasattr(scheduling, 'note'):
        messages.warning(request, f"A Nota de Serviço para o Agendamento {pk} já foi emitida.")
        return redirect('scheduling_list')
    if scheduling.status != 'Sim':
        messages.warning(request, f"Não é possível emitir a nota. O Agendamento {pk} está com pagamento pendente.")
        return redirect('scheduling_list')
    new_note = Note.objects.create(scheduling=scheduling)
    messages.success(request, f"Nota de Serviço Nº {new_note.note_number} gerada com sucesso!")
    return redirect('note_detail', pk=new_note.pk)

@method_decorator(login_required, name='dispatch')
class NoteDetailView(DetailView):
    model = Note
    template_name = 'note_detail.html'
    context_object_name = 'note'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        note = context['note']
        discount_amount = note.scheduling.gross_total_value - note.scheduling.total_value
        context['discount_amount'] = discount_amount
        return context

@login_required(login_url='login')
def note_print_view(request, pk):
    note = get_object_or_404(Note, pk=pk)
    discount_amount = note.scheduling.gross_total_value - note.scheduling.total_value
    return render(request, 'note_print.html', {'note': note, 'discount_amount': discount_amount})

# ==================================================================================== #
# 7. Links do Footer
# ==================================================================================== #

def politica_privacidade(request):
    return render(request, 'politica_privacidade.html')

def termos_de_uso(request):
    return render(request, 'termos_de_uso.html')

def faq(request):
    return render(request, 'faq.html')

def contato(request):
    return render(request, 'contato.html')