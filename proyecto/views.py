from django.db.models import Count
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Tecnico, CategoriaTicket, Ticket, AsignacionTicket
from .serializers import (
    TecnicoSerializer,
    CategoriaTicketSerializer,
    TicketSerializer,
    AsignacionTicketSerializer,
)


class TecnicoViewSet(viewsets.ModelViewSet):
    queryset = Tecnico.objects.all()
    serializer_class = TecnicoSerializer
    search_fields = ["nombre", "apellido", "email"]
    ordering_fields = ["nombre", "apellido"]


class CategoriaTicketViewSet(viewsets.ModelViewSet):
    queryset = CategoriaTicket.objects.all()
    serializer_class = CategoriaTicketSerializer
    search_fields = ["nombre"]
    ordering_fields = ["nombre", "prioridad_default"]


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.select_related("categoria").all()
    serializer_class = TicketSerializer
    search_fields = ["codigo", "titulo", "categoria__nombre"]
    ordering_fields = ["fecha_reporte", "estado"]


class AsignacionTicketListCreateAPIView(generics.ListCreateAPIView):
    queryset = AsignacionTicket.objects.select_related("ticket", "tecnico").all()
    serializer_class = AsignacionTicketSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        estado = self.request.GET.get("estado")
        if estado:
            queryset = queryset.filter(ticket__estado=estado)
        return queryset


@api_view(["GET"])
def resumen_tickets(request):
    total = Ticket.objects.count()
    abiertos = Ticket.objects.filter(estado="abierto").count()
    en_proceso = Ticket.objects.filter(estado="en_proceso").count()
    cerrados = Ticket.objects.filter(estado="cerrado").count()

    por_categoria = Ticket.objects.values("categoria__nombre").annotate(
        total=Count("id")
    ).order_by("-total")

    return Response(
        {
            "total_tickets": total,
            "abiertos": abiertos,
            "en_proceso": en_proceso,
            "cerrados": cerrados,
            "por_categoria": list(por_categoria),
        },
        status=status.HTTP_200_OK,
    )