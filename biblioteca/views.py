from django.shortcuts import render

def inicio(request):
    # Por ahora solo renderizará un archivo HTML simple
    return render(request, 'biblioteca/index.html')