from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    TecnicoViewSet,
    CategoriaTicketViewSet,
    TicketViewSet,
    AsignacionTicketListCreateAPIView,
    resumen_tickets,
)

router = DefaultRouter()
router.register(r"tecnicos", TecnicoViewSet, basename="tecnicos")
router.register(r"categorias", CategoriaTicketViewSet, basename="categorias")
router.register(r"tickets", TicketViewSet, basename="tickets")

urlpatterns = [
    path("", include(router.urls)),
    path("asignaciones/", AsignacionTicketListCreateAPIView.as_view(), name="asignaciones"),
    path("resumen/", resumen_tickets, name="resumen"),
]