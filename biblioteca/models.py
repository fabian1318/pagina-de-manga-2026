from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Genero(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    # El slug sirve para crear URLs amigables como /genero/accion/
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Género"
        verbose_name_plural = "Géneros"

    def __str__(self):
        return self.nombre


class Manga(models.Model):
    ESTADO_CHOICES = [
        ('emision', 'En Emisión'),
        ('finalizado', 'Finalizado'),
        ('pausa', 'En Pausa'),
    ]

    titulo = models.CharField(max_length=200, unique=True)
    autor = models.CharField(max_length=150, default="Anónimo")
    # Sinopsis, descripción o reseña (usamos TextField porque es texto largo)
    sinopsis = models.TextField()
    portada = models.ImageField(upload_to='portadas_manga/')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='emision')
    
    # Calificación: Guarda números como 4.50. Máximo 5.00 y mínimo 0.00
    calificacion = models.DecimalField(
        max_length=5,
        max_digits=3, 
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0.00), MaxValueValidator(5.00)]
    )
    
    # Relación Muchos a Muchos con la tabla Genero
    generos = models.ManyToManyField(Genero, related_name='mangas')
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo