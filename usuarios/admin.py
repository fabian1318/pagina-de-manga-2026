from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

# Esto permite que el panel de administración maneje contraseñas encriptadas correctamente
admin.site.register(Usuario, UserAdmin)
