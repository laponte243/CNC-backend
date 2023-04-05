from .models import *
from django.contrib import admin

# Register your models here.
admin.site.register(Paciente)
admin.site.register(Factura)
admin.site.register(Examen)
admin.site.register(Examen_detalle)