from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Manga

@login_required
def inicio(request):
    # Traemos todos los mangas, ordenados por los más recientes primero
    lista_mangas = Manga.objects.all().order_by('-fecha_agregado')
    
    # Empaquetamos los datos en un "diccionario de contexto" para enviarlos al HTML
    contexto = {
        'mangas': lista_mangas
    }
    
    return render(request, 'biblioteca/index.html', contexto)