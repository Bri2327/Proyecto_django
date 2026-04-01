from rest_framework import serializers
from .models import Tecnico, CategoriaTicket, Ticket, AsignacionTicket


class TecnicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tecnico
        fields = "__all__"


class CategoriaTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaTicket
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source="categoria.nombre", read_only=True)

    class Meta:
        model = Ticket
        fields = "__all__"


class AsignacionTicketSerializer(serializers.ModelSerializer):
    tecnico_nombre = serializers.SerializerMethodField()
    ticket_codigo = serializers.CharField(source="ticket.codigo", read_only=True)

    class Meta:
        model = AsignacionTicket
        fields = "__all__"

    def get_tecnico_nombre(self, obj):
        return f"{obj.tecnico.nombre} {obj.tecnico.apellido}"