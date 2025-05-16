from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User # Si quieres asociar portafolios a usuarios

# Modelo principal para el Portafolio (o CV)
class Portfolio(models.Model):
    # Si quieres que cada usuario tenga su propio portafolio:
    # user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre_completo = models.CharField(max_length=200, help_text="Nombre completo tal como aparecerá en el CV")
    titulo_cv = models.CharField(max_length=255, help_text="Ej: Desarrollador Full Stack, Ingeniero de Software")
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Portafolio de {self.nombre_completo}"

    def get_absolute_url(self):
        return reverse('portfolio_detail', kwargs={'pk': self.pk})

# 1. Datos Personales y de Contacto
class DatosPersonales(models.Model):
    portfolio = models.OneToOneField(Portfolio, on_delete=models.CASCADE, related_name='datos_personales')
    # nombre_completo ya está en el modelo Portfolio
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=255, help_text="Correo electrónico profesional")
    ubicacion = models.CharField(max_length=100, help_text="Ciudad y país de residencia")
    linkedin_url = models.URLField(blank=True, null=True, help_text="Enlace a tu perfil de LinkedIn")
    github_url = models.URLField(blank=True, null=True, help_text="Enlace a tu perfil de GitHub")
    website_url = models.URLField(blank=True, null=True, help_text="Enlace a tu portfolio personal o blog")

    def __str__(self):
        return f"Datos de Contacto de {self.portfolio.nombre_completo}"

# 2. Perfil Profesional o Resumen
class PerfilProfesional(models.Model):
    portfolio = models.OneToOneField(Portfolio, on_delete=models.CASCADE, related_name='perfil_profesional')
    resumen = models.TextField(help_text="Un breve resumen de tu perfil y objetivos profesionales.")

    def __str__(self):
        return f"Perfil Profesional de {self.portfolio.nombre_completo}"

# 3. Experiencia Laboral
class ExperienciaLaboral(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='experiencias_laborales')
    puesto = models.CharField(max_length=200)
    empresa = models.CharField(max_length=200)
    ubicacion_empresa = models.CharField(max_length=100, blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True, help_text="Dejar en blanco si es el trabajo actual")
    descripcion = models.TextField(help_text="Responsabilidades y logros clave. Usa viñetas si es posible.")
    orden = models.PositiveIntegerField(default=0, help_text="Para ordenar las experiencias (más reciente primero)")

    class Meta:
        ordering = ['-fecha_inicio', '-orden'] # Orden cronológico inverso

    def __str__(self):
        return f"{self.puesto} en {self.empresa}"

# 4. Proyectos Personales o Portfolio
class Proyecto(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='proyectos')
    nombre_proyecto = models.CharField(max_length=200)
    descripcion_proyecto = models.TextField()
    tecnologias_utilizadas = models.CharField(max_length=300, help_text="Ej: Python, Django, React, PostgreSQL")
    repositorio_url = models.URLField(blank=True, null=True, help_text="Enlace al repositorio (GitHub, GitLab)")
    demo_url = models.URLField(blank=True, null=True, help_text="Enlace a la demo en vivo")
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return self.nombre_proyecto

# 5. Habilidades (Skills)
class Habilidad(models.Model):
    TIPO_HABILIDAD_CHOICES = [
        ('LENGUAJE', 'Lenguaje de Programación'),
        ('FRAMEWORK', 'Framework/Librería'),
        ('BASE_DATOS', 'Base de Datos'),
        ('HERRAMIENTA', 'Herramienta/Tecnología'),
        ('METODOLOGIA', 'Metodología de Trabajo'),
        ('BLANDA', 'Habilidad Blanda'),
    ]
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='habilidades')
    nombre_habilidad = models.CharField(max_length=100)
    tipo_habilidad = models.CharField(max_length=20, choices=TIPO_HABILIDAD_CHOICES)
    nivel = models.CharField(max_length=50, blank=True, null=True, help_text="Ej: Básico, Intermedio, Avanzado, Experto") # Opcional

    def __str__(self):
        return f"{self.get_tipo_habilidad_display()}: {self.nombre_habilidad}"

# 6. Formación Académica
class FormacionAcademica(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='formaciones_academicas')
    titulo_obtenido = models.CharField(max_length=255)
    institucion = models.CharField(max_length=255)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True, help_text="Dejar en blanco si está en curso")
    menciones = models.TextField(blank=True, null=True, help_text="Menciones honoríficas o logros académicos")
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-fecha_fin', '-orden']

    def __str__(self):
        return f"{self.titulo_obtenido} en {self.institucion}"

# 7. Cursos y Certificaciones
class CursoCertificacion(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='cursos_certificaciones')
    nombre_curso = models.CharField(max_length=255)
    institucion_emisora = models.CharField(max_length=255)
    fecha_obtencion = models.DateField(blank=True, null=True)
    # Para el certificado, puedes usar un FileField o un URLField
    # Usaremos URLField para simplificar, pero FileField es mejor para subir archivos.
    # Para FileField, necesitarías configurar MEDIA_ROOT y MEDIA_URL en settings.py
    certificado_url = models.URLField(blank=True, null=True, help_text="Enlace al certificado (PDF, imagen)")
    # certificado_archivo = models.FileField(upload_to='certificados/', blank=True, null=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-fecha_obtencion', 'orden']

    def __str__(self):
        return self.nombre_curso

# 8. Idiomas
class Idioma(models.Model):
    NIVEL_IDIOMA_CHOICES = [
        ('NATIVO', 'Nativo'),
        ('A1', 'A1 - Principiante'),
        ('A2', 'A2 - Elemental'),
        ('B1', 'B1 - Intermedio bajo'),
        ('B2', 'B2 - Intermedio'),
        ('C1', 'C1 - Intermedio alto'),
        ('C2', 'C2 - Avanzado'),
    ]
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='idiomas')
    nombre_idioma = models.CharField(max_length=50)
    nivel = models.CharField(max_length=10, choices=NIVEL_IDIOMA_CHOICES)

    def __str__(self):
        return f"{self.nombre_idioma}: {self.get_nivel_display()}"

# Secciones Opcionales (Ejemplo con Objetivo Profesional)
class ObjetivoProfesional(models.Model):
    portfolio = models.OneToOneField(Portfolio, on_delete=models.CASCADE, related_name='objetivo_profesional', blank=True, null=True)
    descripcion = models.TextField(help_text="Particularmente útil para perfiles junior o si estás cambiando de carrera.")

    def __str__(self):
        return f"Objetivo Profesional de {self.portfolio.nombre_completo}"

# Puedes añadir más modelos para Publicaciones, Conferencias, Voluntariado, Intereses de manera similar.
# Por ejemplo:
class PublicacionConferencia(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='publicaciones_conferencias')
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True) # Ej: "Presentado en Conferencia X", "Publicado en Revista Y"
    fecha = models.DateField(blank=True, null=True)
    enlace = models.URLField(blank=True, null=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-fecha', 'orden']

    def __str__(self):
        return self.titulo

class Voluntariado(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='voluntariados')
    organizacion = models.CharField(max_length=200)
    puesto_rol = models.CharField(max_length=200)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-fecha_inicio', 'orden']

    def __str__(self):
        return f"{self.puesto_rol} en {self.organizacion}"

class InteresHobby(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='intereses_hobbies')
    nombre = models.CharField(max_length=100)
    descripcion_breve = models.CharField(max_length=255, blank=True, null=True, help_text="Si es relevante o muestra habilidades transferibles")

    def __str__(self):
        return self.nombre