from django.urls import path

from . import views

urlpatterns = [
    path('contact/<str:name>', views.contact),
    path('categorias', views.categorias, name='categorias'),
    path('productos', views.productoFormView),
    path('clase8', views.index),
]
