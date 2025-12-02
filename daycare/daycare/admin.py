from django.contrib import admin
from .models import Tutor, Pet, Service, State, City, Scheduling, Note


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ('name', 'cpf', 'state', 'city', 'email')
    search_fields = ('name', 'cpf', 'email')
    list_filter = ('state',)


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'race', 'get_sex', 'tutor')
    list_filter = ('sex',)

    def get_sex(self, obj):
        return obj.get_sex_display()
    get_sex.short_description = 'Sexo'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price')


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'state')


@admin.register(Scheduling)
class SchedulingAdmin(admin.ModelAdmin):
    list_display = ('id', 'pet', 'tutor', 'date_scheduling', 'gross_total_value', 'percentage_discount', 'total_value')
    filter_horizontal = ('services',)
    readonly_fields = ('gross_total_value', 'total_value')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.calculate_values()
        obj.save()

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        obj = form.instance
        obj.calculate_values()
        obj.save()


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):  
    list_display = ('note_number', 'scheduling', 'issue_date')
