from django.db import models

class Paciente(models.Model):
    nacionalidad = models.TextField(max_length=50, null=True)
    documento = models.TextField(max_length=50, null=True)
    cedula = models.TextField(max_length=20, null=False)
    nombre = models.TextField(max_length=50, null=False)
    apellido = models.TextField(max_length=50, null=False) 
    sexo = models.TextField(max_length=2, null=False)
    fecha_nacimiento = models.DateField(null=False)
    direccion = models.TextField(max_length=50, null=True)
    telefono = models.TextField(max_length=50, null=True)
    correo = models.TextField(max_length=20, null= True)

class Factura(models.Model):
    numero_factura = models.TextField(max_length=50, null=False) 
    paciente = models.ForeignKey(Paciente, null=True, on_delete=models.DO_NOTHING)

class Examen(models.Model):
    paciente = models.ForeignKey(Paciente, null=True, on_delete=models.DO_NOTHING)
    factura = models.ForeignKey(Factura, null=True, on_delete=models.DO_NOTHING)
    seccion =  models.TextField(max_length=50, null=False)
    codigo = models.TextField(max_length=20, null=False)
    status = models.TextField(max_length=5, null=False)
    descripcion = models.TextField(max_length=50, null=False)
    resultado = models.TextField(max_length=50, null=True)
    unidad = models.TextField(max_length=50, null=True)
    valor_referencia = models.TextField(max_length=50, null=True)
    observaciones = models.TextField(max_length=50, null=True)

class Examen_detalle(models.Model): 
    id_examen = models.ForeignKey(Examen, null=True, on_delete=models.DO_NOTHING)
    codigo = models.TextField(max_length=20, null=False)
    status = models.TextField(max_length=5, null=False)
    descripcion = models.TextField(max_length=50, null=True)
    resultado = models.TextField(max_length=50, null=True)
    unidad = models.TextField(max_length=50, null=True)
    valor_referencia = models.TextField(max_length=50, null=True)
