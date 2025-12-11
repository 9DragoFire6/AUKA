from django.contrib import admin
from .models import Categoria, Producto, Servicio, Evento, Publicacion

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio_referencia', 'activo']
    list_filter = ['categoria', 'activo']
    search_fields = ['nombre', 'descripcion']

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'duracion']
    search_fields = ['nombre', 'descripcion']

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'fecha', 'ubicacion', 'activo']
    list_filter = ['activo', 'fecha']
    search_fields = ['titulo', 'descripcion']

@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    list_display = ("titulo", "fuente", "fecha_publicacion", "activo")  # 👈 muestra el checkbox
    list_filter = ("fuente", "fecha_publicacion", "activo")
    search_fields = ("titulo", "contenido")
    list_editable = ("activo",)  # 👈 permite editar el campo directamente en la lista
    ordering = ("-fecha_publicacion",)
