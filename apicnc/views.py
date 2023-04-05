from django.shortcuts import render
import xmltodict, json
import datetime
from django.template.loader import get_template
import os
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse, HttpResponse 
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from .serializers import *
from apicnc import archivos as files
from django.views.generic import View
# Create your views here.
import weasyprint
from weasyprint.text.fonts import FontConfiguration
from django.template.loader import render_to_string
from xhtml2pdf import pisa

@permission_classes([AllowAny])
class PacienteViewset(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

@permission_classes([AllowAny])
class ExamenViewset(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Examen.objects.all()
    serializer_class = ExamenSerializer

@permission_classes([AllowAny])
class  FacturaViewset(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer

@permission_classes([AllowAny])
class Examen_detalleViewset(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Examen_detalle.objects.all()
    serializer_class = Examen_detalleSerializer

def Convertidor(request):
    try:
        for filename in os.listdir('apicnc/archivos'):
            with open('apicnc/archivos/' + filename,'r') as myfile:
                obj = xmltodict.parse(myfile.read())
                archivo = json.dumps(obj)
                try:
                    pacientes = Paciente.objects.get(cedula=obj['infolab']['paciente']['cedula'])
                except Paciente.DoesNotExist:
                    pacientes = Paciente(
                        nacionalidad = obj['infolab']['paciente']['nacionalidad'],
                        documento  = obj['infolab']['paciente']['documento'],
                        cedula = obj['infolab']['paciente']['cedula'],
                        nombre = obj['infolab']['paciente']['nombre'],
                        apellido =  obj['infolab']['paciente']['apellido'],
                        sexo = obj['infolab']['paciente']['sexo'],
                        fecha_nacimiento = datetime.datetime.strptime( obj['infolab']['paciente']['fecha-nacimiento'], "%d/%m/%Y").strftime('%Y-%m-%d'),
                        direccion = obj['infolab']['paciente']['direccion'],
                        telefono = obj['infolab']['paciente']['telefono'],
                        correo  = obj['infolab']['paciente']['email'],
                    )
                    print(pacientes)
                    pacientes.save()
                try:
                    facturax = Factura.objects.get(numero_factura= obj['infolab']['factura']['id'])
                except Factura.DoesNotExist:
                    facturax = Factura(
                        paciente= pacientes,
                        numero_factura = obj['infolab']['factura']['id'],
                    )
                    facturax.save()
                    print(facturax)
            if Examen.objects.filter(factura = facturax).count() > 0:
                print('no')
                
            else:
                for item in obj['infolab']['examen']:
                    examenx = Examen( 
                    paciente = pacientes,
                    factura = facturax,
                    seccion =item['seccion'],
                    codigo = item['codigo'],
                    status = item['status'],
                    descripcion = item['descripcion'],
                    resultado = item['resultado'],
                    unidad = item['unidad'],
                    valor_referencia = item['valreferencia'],
                    observaciones = item['observaciones'],
                    )
                    examenx.save()
                    try:
                        for detalle in item['examend']:
                            examex_d = Examen_detalle(
                                id_examen = examenx,
                                codigo = detalle['codigo'],
                                status = detalle['status'],
                                descripcion = detalle['descripcion'],
                                resultado = detalle['resultado'],
                                unidad = detalle['unidad'],
                                valor_referencia = detalle['valreferencia'],
                            )
                            examex_d.save()
                    except Exception as e:
                            print(e)
        return JsonResponse(obj['infolab']['examen'], safe=False, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def GeneratePdf(request):
    pdf = render_to_pdf('example.html')
    return HttpResponse(pdf, content_type='application/pdf')

def testing(request):
    paciente = Paciente.objects.get(id=2)
    examenes = Examen.objects.filter(factura__paciente=paciente).prefetch_related('examen_detalle_set').all()
    
    context = {"paciente":paciente,"examenes":examenes}
    template_name = 'example.html'
    return render(request, template_name,context)

def export_pdf(request,id_paciente):
    paciente = Paciente.objects.get(id=id_paciente)
    examenes = Examen.objects.filter(factura__paciente=paciente).prefetch_related('examen_detalle_set').all()
    
    context = {"paciente":paciente,"examenes":examenes}
    html = render_to_string("template_mail.html", context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; report.pdf"

    font_config = FontConfiguration()
    weasyprint.HTML(string=html).write_pdf(response, font_config=font_config)

    return response

def testing2(request):
     # Render the HTML template
    template = get_template('template_mail.html')
    html_string = template.render()

    # Generate the PDF using WeasyPrint
    pdf = weasyprint.HTML(string=html_string).write_pdf()

    # Set the response content type to PDF
    response = HttpResponse(pdf, content_type='application/pdf')

    # Set the filename and content disposition
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    return response



def testing22(request):
    # Obtener el template
    template = get_template('template_mail.html')

    # Renderizar el template con los datos que necesites
    context = {'report_data': 'Datos del reporte'}
    html = template.render(context)

    # Crear un objeto HttpResponse con el PDF generado
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    # Convertir el HTML a PDF utilizando la librería xhtml2pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF: %s' % pisa_status.err)

    return response