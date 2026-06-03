from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    # Hereda campos como username, email, password, first_name, last_name.
    # Añadimos un campo extra de ejemplo por si deseas segmentar roles más adelante
    es_administrador = models.BooleanField(default=False)

    def __str__(self):
        return self.username