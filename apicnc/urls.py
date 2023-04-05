from django.urls import path, include
from rest_framework.authtoken import views as vx
from rest_framework import routers
from django.conf import settings
from . import views

router = routers.DefaultRouter()
router.register(r'Pacientes', views.PacienteViewset),
router.register(r'Examen', views.ExamenViewset),
router.register(r'Examen_detalle', views.Examen_detalleViewset)
router.register(r'Factura', views.FacturaViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', vx.obtain_auth_token),
    path('convertidor/', views.Convertidos),
    path('test/', views.testing),
    path('export/<int:id_paciente>', views.export_pdf, name="export-pdf" )
]