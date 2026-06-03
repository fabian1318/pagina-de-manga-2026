from django.contrib import admin
from django.path import path, include 

urlpatterns = [
    path('admin/', admin.site.get_urls()),
    
    # Esto activa automáticamente rutas como /usuarios/login/ y /usuarios/logout/
    path('usuarios/', include('django.contrib.auth.urls')),

]