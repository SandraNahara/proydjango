from django.contrib import admin
from .models import (
    Portfolio, DatosPersonales, PerfilProfesional, ExperienciaLaboral,
    Proyecto, Habilidad, FormacionAcademica, CursoCertificacion, Idioma,
    ObjetivoProfesional, PublicacionConferencia, Voluntariado, InteresHobby
)

# Para mejorar la visualización y gestión en el admin, podemos usar 'inlines'
# Esto permite editar modelos relacionados directamente desde la página del modelo principal (Portfolio)

class DatosPersonalesInline(admin.StackedInline): # o admin.TabularInline para una vista más compacta
    model = DatosPersonales
    can_delete = False # No permitir borrar desde el inline si es OneToOne y requerido
    verbose_name_plural = 'Datos Personales'

class PerfilProfesionalInline(admin.StackedInline):
    model = PerfilProfesional
    can_delete = False
    verbose_name_plural = 'Perfil Profesional'

class ObjetivoProfesionalInline(admin.StackedInline):
    model = ObjetivoProfesional
    can_delete = False
    verbose_name_plural = 'Objetivo Profesional (Opcional)'
    extra = 0 # No mostrar formularios vacíos por defecto si no existe

class ExperienciaLaboralInline(admin.TabularInline):
    model = ExperienciaLaboral
    extra = 1 # Mostrar 1 formulario vacío para añadir
    ordering = ('-fecha_inicio',)

class ProyectoInline(admin.TabularInline):
    model = Proyecto
    extra = 1
    ordering = ('orden',)

class HabilidadInline(admin.TabularInline):
    model = Habilidad
    extra = 1

class FormacionAcademicaInline(admin.TabularInline):
    model = FormacionAcademica
    extra = 1
    ordering = ('-fecha_fin',)

class CursoCertificacionInline(admin.TabularInline):
    model = CursoCertificacion
    extra = 1
    ordering = ('-fecha_obtencion',)

class IdiomaInline(admin.TabularInline):
    model = Idioma
    extra = 1

class PublicacionConferenciaInline(admin.TabularInline):
    model = PublicacionConferencia
    extra = 1
    ordering = ('-fecha',)

class VoluntariadoInline(admin.TabularInline):
    model = Voluntariado
    extra = 1
    ordering = ('-fecha_inicio',)

class InteresHobbyInline(admin.TabularInline):
    model = InteresHobby
    extra = 1

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'titulo_cv', 'creado_en', 'actualizado_en')
    search_fields = ('nombre_completo', 'titulo_cv')
    inlines = [
        DatosPersonalesInline,
        PerfilProfesionalInline,
        ObjetivoProfesionalInline,
        ExperienciaLaboralInline,
        ProyectoInline,
        HabilidadInline,
        FormacionAcademicaInline,
        CursoCertificacionInline,
        IdiomaInline,
        PublicacionConferenciaInline,
        VoluntariadoInline,
        InteresHobbyInline,
    ]
