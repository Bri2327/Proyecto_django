from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .forms import ProductoForm
from .models import Categoria, Producto


def index(request):
    return HttpResponse("Hola mundo")


def contact(request, name):
    return HttpResponse(f"Hola {name} bienvenido a la clase de Django")


def categorias(request):
    post_nombre = request.POST.get('nombre')
    if post_nombre:
        q = Categoria(nombre=post_nombre)
        q.save()

    nombre_filtro = request.GET.get('nombre')
    if nombre_filtro:
        categorias = Categoria.objects.filter(nombre__contains=nombre_filtro)
    else:
        categorias = Categoria.objects.all()

    return render(request, 'form_categorias.html', {
        "categorias": categorias
    })


def productoFormView(request):
    form = ProductoForm()
    producto = None
    id_producto = request.GET.get('id')
    if id_producto:
        # producto = Producto.objects.get(id=id_producto)
        producto = get_object_or_404(Producto, id=id_producto)
        form = ProductoForm(instance=producto)

    if request.method == 'POST':
        if producto:
            form = ProductoForm(request.POST, instance=producto)
        else:
            form = ProductoForm(request.POST)

    if form.is_valid():
        form.save()

    return render(request, 'form_productos.html', {
        "form": form
    })
