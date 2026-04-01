from django.contrib import admin

from .models import Categoria, Producto

admin.site.register(Categoria)


class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'unidades', 'precio')
    ordering = ('precio',)
    search_fields = ('nombre',)
    list_filter = ('unidades',)


admin.site.register(Producto, ProductoAdmin)