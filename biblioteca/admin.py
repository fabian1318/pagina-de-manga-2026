from django.contrib import admin
from .models import Manga, Genero, Capitulo, Pagina

@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    # Esto autocompleta el slug cuando escribes el nombre del género
    prepopulated_fields = {'slug': ('nombre',)}

@admin.register(Manga)
class MangaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'estado', 'calificacion', 'fecha_agregado')
    list_filter = ('estado', 'generos')
    search_fields = ('titulo', 'autor')

@admin.register(Capitulo)
class CapituloAdmin(admin.ModelAdmin):
    # Añadimos 'tomo' a la vista
    list_display = ('manga', 'tomo', 'numero', 'titulo', 'fecha_subida')
    list_filter = ('manga', 'tomo')

@admin.register(Pagina)
class PaginaAdmin(admin.ModelAdmin):
    list_display = ('capitulo', 'numero')
    list_filter = ('capitulo__manga', 'capitulo')
    