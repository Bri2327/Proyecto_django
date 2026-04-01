from django.contrib import admin
from .models import Tecnico, CategoriaTicket, Ticket, AsignacionTicket


@admin.register(Tecnico)
class TecnicoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "apellido", "email", "telefono")
    search_fields = ("nombre", "apellido", "email")


@admin.register(CategoriaTicket)
class CategoriaTicketAdmin(admin.ModelAdmin):
    list_display = ("nombre", "prioridad_default")
    search_fields = ("nombre",)
    list_filter = ("prioridad_default",)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("codigo", "titulo", "categoria", "estado", "urgente", "fecha_reporte")
    search_fields = ("codigo", "titulo")
    list_filter = ("estado", "urgente", "categoria")


@admin.register(AsignacionTicket)
class AsignacionTicketAdmin(admin.ModelAdmin):
    list_display = ("ticket", "tecnico", "fecha_asignacion", "atendido")
    search_fields = ("ticket__codigo", "ticket__titulo", "tecnico__nombre", "tecnico__apellido")
    list_filter = ("atendido",)