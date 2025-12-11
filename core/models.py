from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    descripcion = models.TextField()
    precio_referencia = models.DecimalField(max_digits=10, decimal_places=2)
    fotografia = models.ImageField(upload_to='productos/')
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
    
    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

class Servicio(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    duracion = models.CharField(max_length=50)
    beneficios = models.TextField()
    
    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
    
    def __str__(self):
        return self.nombre

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha = models.DateTimeField()
    ubicacion = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to='eventos/', blank=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
    
    def __str__(self):
        return self.titulo

from django.db import models

class Publicacion(models.Model):
    FUENTES = [
        ("Blog", "Blog"),
        ("Facebook", "Facebook"),
        ("Instagram", "Instagram"),
    ]

    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to="publicaciones/", blank=True, null=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    fuente = models.CharField(max_length=20, choices=FUENTES, default="Blog")
    url_original = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ["-fecha_publicacion"]

    def __str__(self):
        return f"{self.titulo} ({self.fuente})"

class Publicacion(models.Model):
    FUENTES = [
        ("Blog", "Blog"),
        ("Facebook", "Facebook"),
        ("Instagram", "Instagram"),
    ]

    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to="publicaciones/", blank=True, null=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    fuente = models.CharField(max_length=20, choices=FUENTES, default="Blog")
    url_original = models.URLField(blank=True, null=True)
    activo = models.BooleanField(default=True)  # 👈 aquí va el campo nuevo

    class Meta:
        ordering = ["-fecha_publicacion"]

    def __str__(self):
        return f"{self.titulo} ({self.fuente})"
