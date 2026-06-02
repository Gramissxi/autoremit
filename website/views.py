from django.shortcuts import render
from django.http import JsonResponse
from .models import Consulta

def inicio(request):
    return render(request, 'website/inicio.html')



def guardar_consulta(request):

    if request.method == 'POST':

        nombre = request.POST.get('nombre')

        empresa = request.POST.get('empresa')

        telefono = request.POST.get('telefono')

        mensaje = request.POST.get('mensaje')

        Consulta.objects.create(
            nombre=nombre,
            empresa=empresa,
            telefono=telefono,
            mensaje=mensaje
        )

        return JsonResponse({
            'status': 'ok'
        })