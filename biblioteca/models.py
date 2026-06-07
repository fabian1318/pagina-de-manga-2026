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
    
class Capitulo(models.Model):
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, related_name='capitulos')
    
    # NUEVO: Campo de Tomo (Volumen). Puede estar vacío (blank=True, null=True)
    tomo = models.DecimalField(
        max_digits=5, 
        decimal_places=1, 
        blank=True, 
        null=True, 
        help_text="Déjalo en blanco si es un capítulo semanal sin tomo oficial."
    )
    
    numero = models.DecimalField(max_digits=5, decimal_places=1)
    titulo = models.CharField(max_length=200, blank=True, null=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Capítulo"
        verbose_name_plural = "Capítulos"
        # Ordenamos primero por tomo (los sueltos al final) y luego por capítulo
        ordering = ['tomo', '-numero']

    def __str__(self):
        # Un texto dinámico para que el panel de administración se vea ordenado
        texto = f"{self.manga.titulo} - "
        if self.tomo:
            texto += f"Tomo {self.tomo} | "
        texto += f"Cap. {self.numero}"
        if self.titulo:
            texto += f": {self.titulo}"
        return texto
    
class Pagina(models.Model):
    # Relacionamos cada página con su capítulo
    capitulo = models.ForeignKey(Capitulo, on_delete=models.CASCADE, related_name='paginas')
    
    # El número de la página (1, 2, 3...) para que se lean en orden
    numero = models.PositiveIntegerField()
    
    # Aquí se guardará la imagen real de la página
    imagen = models.ImageField(upload_to='mangas/paginas/')

    class Meta:
        verbose_name = "Página"
        verbose_name_plural = "Páginas"
        # Es CRÍTICO que se ordenen por número, sino el manga se leerá desordenado
        ordering = ['numero']

    def __str__(self):
        return f"Página {self.numero} - {self.capitulo}"