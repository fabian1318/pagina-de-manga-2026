from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Manga, Capitulo, Genero, HistorialLectura
from django.http import JsonResponse
import json

@login_required 
def inicio(request):
    # 1. Traemos todos los mangas y todos los géneros (para el menú desplegable)
    mangas = Manga.objects.all().order_by('-fecha_agregado')
    generos = Genero.objects.all()

    # 2. Capturamos lo que el usuario envía por la URL (ej: ?q=naruto&genero=2)
    query = request.GET.get('q')
    genero_id = request.GET.get('genero')

    # 3. Filtramos por texto (Título O Autor) usando 'icontains' (que ignora mayúsculas/minúsculas)
    if query:
        mangas = mangas.filter(
            Q(titulo__icontains=query) | Q(autor__icontains=query)
        ).distinct() # distinct() evita que salgan duplicados

    # 4. Filtramos por género si el usuario seleccionó uno
    if genero_id:
        mangas = mangas.filter(generos__id=genero_id)

    # 5. Enviamos todo al HTML, incluyendo lo que el usuario buscó para que no se borre de la barra
    contexto = {
        'mangas': mangas,
        'generos': generos,
        'query_actual': query if query else '',
        # Convertimos genero_id a número solo si existe, para mantener seleccionado el menú
        'genero_actual': int(genero_id) if genero_id and genero_id.isdigit() else '',
    }
    
    return render(request, 'biblioteca/index.html', contexto)

@login_required
def detalle_manga(request, manga_id):
    manga = get_object_or_404(Manga, id=manga_id)
    capitulos = manga.capitulos.all()
    
    # Buscamos si el usuario ya empezó a leer este manga
    progreso = HistorialLectura.objects.filter(usuario=request.user, manga=manga).first()
    
    contexto = {
        'manga': manga,
        'capitulos': capitulos,
        'progreso': progreso, # <-- Pasamos el progreso al HTML
    }
    return render(request, 'biblioteca/detalle.html', contexto)

@login_required
def leer_capitulo(request, capitulo_id):
    capitulo = get_object_or_404(Capitulo, id=capitulo_id)
    paginas = capitulo.paginas.all()
    
    # Buscamos si ya tiene un progreso guardado para este manga
    progreso = HistorialLectura.objects.filter(usuario=request.user, manga=capitulo.manga).first()
    
    # Si estaba leyendo ESTE mismo capítulo, sacamos la página. Si no, empezamos en la 1.
    pagina_guardada = 1
    if progreso and progreso.capitulo == capitulo:
        pagina_guardada = progreso.pagina_actual
    
    # Actualizamos que abrió el capítulo (sin sobrescribir la página aún)
    HistorialLectura.objects.update_or_create(
        usuario=request.user,
        manga=capitulo.manga,
        defaults={'capitulo': capitulo}
    )
    
    contexto = {
        'capitulo': capitulo,
        'paginas': paginas,
        'pagina_guardada': pagina_guardada # <-- Pasamos este dato vital
    }
    return render(request, 'biblioteca/leer.html', contexto)

@login_required
def guardar_progreso_ajax(request):
    if request.method == 'POST':
        # Recibimos los datos enviados por JavaScript
        data = json.loads(request.body)
        capitulo_id = data.get('capitulo_id')
        pagina_num = data.get('pagina')
        
        capitulo = get_object_or_404(Capitulo, id=capitulo_id)
        
        # Actualizamos la base de datos
        HistorialLectura.objects.update_or_create(
            usuario=request.user,
            manga=capitulo.manga,
            defaults={
                'capitulo': capitulo,
                'pagina_actual': pagina_num
            }
        )
        return JsonResponse({'status': 'guardado'})
    return JsonResponse({'error': 'metodo no permitido'}, status=400)
