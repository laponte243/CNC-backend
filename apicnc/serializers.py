from django.db.models import fields
from rest_framework import serializers
from .models import *



class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'
class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = '__all__'
class ExamenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examen
        fields = '__all__'

class Examen_detalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examen_detalle
        fields = '__all__'

