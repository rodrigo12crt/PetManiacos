from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView 
from .views import (
    home_view, 
    dashboard_view,
    PetCreateView,
    PetUpdateView,
    PetListView, 
    PetDetailView,    
    PetDeleteView,

    TutorCreateView, 
    TutorUpdateView,
    TutorListView,
    TutorDeleteView,
    
    ServiceCreateView,
    ServiceUpdateView,
    ServiceListView,
    ServiceDeleteView,

    SchedulingCreateView, 
    SchedulingUpdateView,
    SchedulingListView, 
    SchedulingDeleteView,

    generate_note_view,
    note_print_view,
    NoteDetailView,

    politica_privacidade,
    termos_de_uso,
    faq,
    contato,
)

urlpatterns = [
    # 1. Dashboard e Home
    path('', home_view, name='home'), 
    path('dashboard/', dashboard_view, name='dashboard'),
    
    # 2. Autenticação
    path('entrar/', LoginView.as_view(template_name='login.html'), name='login'),
    path('sair/', LogoutView.as_view(next_page='login'), name='logout'),
    
    # 3. Pets
    path('pets/novo/', PetCreateView.as_view(), name='pet_create'),
    path('pets/editar/<int:pk>/', PetUpdateView.as_view(), name='pet_update'),
    path('pets/', PetListView.as_view(), name='pet_list'),
    path('pets/<int:pk>/', PetDetailView.as_view(), name='pet_detail'),
    path('pets/excluir/<int:pk>/', PetDeleteView.as_view(), name='pet_delete'),
    
    # 4. Tutores
    path('tutores/novo/', TutorCreateView.as_view(), name='tutor_create'), 
    path('tutores/editar/<int:pk>/', TutorUpdateView.as_view(), name='tutor_update'),
    path('tutores/', TutorListView.as_view(), name='tutor_list'), 
    path('tutores/excluir/<int:pk>/', TutorDeleteView.as_view(), name='tutor_delete'),

    # 5. Serviços
    path('servicos/novo/', ServiceCreateView.as_view(), name='service_create'),
    path('servicos/editar/<int:pk>/', ServiceUpdateView.as_view(), name='service_update'),
    path('servicos/', ServiceListView.as_view(), name='service_list'),
    path('servicos/excluir/<int:pk>/', ServiceDeleteView.as_view(), name='service_delete'),

    # 6. Agendamentos
    path('agendamentos/novo/', SchedulingCreateView.as_view(), name='scheduling_create'),
    path('agendamentos/editar/<int:pk>/', SchedulingUpdateView.as_view(), name='scheduling_update'),
    path('agendamentos/', SchedulingListView.as_view(), name='scheduling_list'),
    path('agendamentos/excluir/<int:pk>/', SchedulingDeleteView.as_view(), name='scheduling_delete'),
    
    # 7. Notas de Serviço
    path('agendamentos/gerar-nota/<int:pk>/', generate_note_view, name='generate_note'),
    path('nota/<int:pk>/', NoteDetailView.as_view(), name='note_detail'),
    path('nota/<int:pk>/print/', note_print_view, name='note_print'),

    # 8. Links do Footer
    path('politica-de-privacidade/', politica_privacidade, name='politica_privacidade'),
    path('termos-de-uso/', termos_de_uso, name='termos_de_uso'),
    path('faq/', faq, name='faq'),
    path('contato/', contato, name='contato'),
]
