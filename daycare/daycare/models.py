from django.db import models
from django.db.models import Sum
from decimal import Decimal
from smart_selects.db_fields import ChainedForeignKey

class State(models.Model):
    name = models.CharField(max_length=100, verbose_name='Estado')
    abbreviation = models.CharField(max_length=2, unique=True, verbose_name='Sigla')

    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"

    def __str__(self):
        return self.name


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, verbose_name='Estado')
    name = models.CharField(max_length=100, verbose_name='Cidade')

    class Meta:
        verbose_name = "Cidade"
        verbose_name_plural = "Cidades"

    def __str__(self):
        return self.name


class Tutor(models.Model):
    ORIGEM_CHOICES = [
        ('internet', 'Internet'),
        ('amigo', 'Amigo'),
        ('indicacao_veterinario', 'Indicação de Veterinário'),
        ('redes_sociais', 'Redes Sociais'),
        ('panfleto', 'Panfleto / Outdoor'),
        ('passando_na_rua', 'Passando na Rua'),
        ('evento_pet', 'Evento Pet'),
        ('outro', 'Outro'),
    ]

    name = models.CharField(max_length=255, verbose_name='Nome')
    cpf = models.CharField(max_length=14, unique=True, verbose_name='CPF')
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Telefone')
    email = models.EmailField(blank=True, null=True, verbose_name='Email')
    address = models.TextField(blank=True, null=True, verbose_name='Endereço')
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Estado')
    city = ChainedForeignKey(
        City,
        chained_field="state",
        chained_model_field="state",
        verbose_name='Cidade',
        show_all=False,
        auto_choose=True,
        sort=True,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    know = models.CharField(max_length=50, choices=ORIGEM_CHOICES, blank=True, null=True, verbose_name='Como Conheceu')

    class Meta:
        verbose_name = "Tutor"
        verbose_name_plural = "Tutores"

    def __str__(self):
        return self.name


class Pet(models.Model):
    ORIGEM_SEX = [
        ('macho', 'Macho'),
        ('femea', 'Fêmea'),
    ]

    name = models.CharField(max_length=100, verbose_name='Nome')
    species = models.CharField(max_length=100, verbose_name='Espécie')
    race = models.CharField(max_length=100, blank=True, null=True, verbose_name='Raça')
    age = models.CharField(max_length=50, blank=True, null=True, verbose_name='Idade')
    sex = models.CharField(max_length=20, choices=ORIGEM_SEX, blank=True, verbose_name='Sexo')
    weight = models.FloatField(blank=True, null=True, verbose_name='Peso')
    medical_observations = models.TextField(blank=True, null=True, verbose_name='Observações Médicas')
    photo = models.ImageField(upload_to='pets/', blank=True, null=True, verbose_name='Foto')
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, verbose_name='Nome do Tutor')

    class Meta:
        verbose_name = "Pet"
        verbose_name_plural = "Pets"

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nome')
    description = models.TextField(blank=True, null=True, verbose_name='Descrição')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço')

    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'

    def __str__(self):
        return f"{self.name} - R$ {self.price:.2f}"


class Scheduling(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, verbose_name='Nome do Tutor')
    pet = ChainedForeignKey(
        'Pet', 
        chained_field="tutor", 
        chained_model_field="tutor", 
        verbose_name='Nome do Pet',
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.CASCADE
)
    services = models.ManyToManyField(Service, verbose_name='Serviços')
    date_scheduling = models.DateField(verbose_name='Data do Agendamento')
    status = models.CharField(max_length=20, choices=[('Sim', 'Sim'), ('Não', 'Não')], verbose_name='Status de Pagamento')
    observations = models.TextField(blank=True, null=True, verbose_name='Observações')
    percentage_discount = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Desconto Percentual')
    gross_total_value = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Valor Bruto Total')
    total_value = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Valor Total')

    def calculate_values(self):
        total = self.services.aggregate(total=Sum('price'))['total'] or Decimal('0.00')
        self.gross_total_value = total
        discount = total * (Decimal(self.percentage_discount) / Decimal('100'))
        self.total_value = total - discount

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    # garante que services já foi salvo antes de calcular valores
        if self.pk:
            self.calculate_values()
            super().save(update_fields=["gross_total_value", "total_value"])


    def __str__(self):
        return f"Agendamento {self.id} - {self.pet.name}"

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'

class Note(models.Model):
    scheduling = models.OneToOneField(Scheduling, on_delete=models.CASCADE, verbose_name='Agendamento')
    note_number = models.AutoField(primary_key=True, verbose_name='Numero da Nota')
    issue_date = models.DateTimeField(auto_now_add=True, verbose_name='Data de Emissão')

    class Meta:
        verbose_name = 'Nota de Atendimento'
        verbose_name_plural = 'Notas'

    def __str__(self):
        return f"Nota {self.note_number}"
