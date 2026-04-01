from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone


def validar_codigo_ticket(value):
    if not value.startswith("TK-"):
        raise ValidationError("El código debe comenzar con TK-")


class Tecnico(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=8, validators=[MinLengthValidator(8)])

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def clean(self):
        if not self.telefono.isdigit():
            raise ValidationError({"telefono": "El teléfono solo debe contener números"})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class CategoriaTicket(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    prioridad_default = models.IntegerField(default=3)

    def __str__(self):
        return self.nombre

    def clean(self):
        if self.prioridad_default < 1 or self.prioridad_default > 5:
            raise ValidationError({"prioridad_default": "La prioridad debe estar entre 1 y 5"})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class EstadoTicket(models.TextChoices):
    ABIERTO = "abierto", "Abierto"
    EN_PROCESO = "en_proceso", "En proceso"
    CERRADO = "cerrado", "Cerrado"


class Ticket(models.Model):
    codigo = models.CharField(max_length=20, unique=True, validators=[validar_codigo_ticket])
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    categoria = models.ForeignKey(CategoriaTicket, on_delete=models.CASCADE)
    fecha_reporte = models.DateField(default=timezone.now)
    fecha_cierre = models.DateField(null=True, blank=True)
    estado = models.CharField(
        max_length=20,
        choices=EstadoTicket.choices,
        default=EstadoTicket.ABIERTO
    )
    urgente = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.codigo} - {self.titulo}"

    def clean(self):
        if self.fecha_cierre and self.fecha_cierre < self.fecha_reporte:
            raise ValidationError({"fecha_cierre": "La fecha de cierre no puede ser anterior a la fecha de reporte"})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class AsignacionTicket(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    tecnico = models.ForeignKey(Tecnico, on_delete=models.CASCADE)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    atendido = models.BooleanField(default=False)
    observacion = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ("ticket", "tecnico")

    def __str__(self):
        return f"{self.ticket.codigo} -> {self.tecnico.nombre} {self.tecnico.apellido}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)