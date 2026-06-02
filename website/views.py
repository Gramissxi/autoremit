from django.shortcuts import render

def inicio(request):
    return render(request, 'website/inicio.html')

def servicios(request):
    return render(request, 'website/servicios.html')

def contacto(request):
    return render(request, 'website/contacto.html')