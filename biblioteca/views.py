from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Manga, Capitulo

@login_required
def inicio(request):
    # Traemos todos los mangas, ordenados por los más recientes primero
    lista_mangas = Manga.objects.all().order_by('-fecha_agregado')
    
    # Empaquetamos los datos en un "diccionario de contexto" para enviarlos al HTML
    contexto = {
        'mangas': lista_mangas
    }
    
    return render(request, 'biblioteca/index.html', contexto)

@login_required
def detalle_manga(request, manga_id):
    # Busca el manga por su ID. Si alguien pone un ID que no existe, lanza error 404 seguro.
    manga = get_object_or_404(Manga, id=manga_id)
    
    # Obtenemos todos los capítulos asociados a este manga
    capitulos = manga.capitulos.all()
    
    contexto = {
        'manga': manga,
        'capitulos': capitulos
    }
    return render(request, 'biblioteca/detalle.html', contexto)

@login_required
def leer_capitulo(request, capitulo_id):
    # Buscamos el capítulo específico
    capitulo = get_object_or_404(Capitulo, id=capitulo_id)
    
    # Gracias a que pusimos ordering=['numero'] en models.py, 
    # esto ya nos trae las imágenes perfectamente ordenadas (1, 2, 3...)
    paginas = capitulo.paginas.all()
    
    contexto = {
        'capitulo': capitulo,
        'paginas': paginas
    }
    return render(request, 'biblioteca/leer.html', contexto)