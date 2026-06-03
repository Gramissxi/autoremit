
from .models import Empresa, Remito, DiaServicio
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RemitoForm
from decimal import Decimal, InvalidOperation
from django.http import HttpResponse
from django.template.loader import get_template
#from xhtml2pdf import pisa
from .models import Remito, DiaServicio
from django.template.loader import render_to_string
#from weasyprint import HTML
from django.http import HttpResponse
from .models import Remito
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    context = {
        'empresas': Empresa.objects.all(),
        'remitos': Remito.objects.all(),
        'dias': DiaServicio.objects.all()
    }
    return render(request, 'remitos/index.html', context)


@login_required
def remito_create(request):
    if request.method == 'POST':
        form = RemitoForm(request.POST)
        if form.is_valid():
            remito = form.save()
            # Redirigir a cargar días para el remito creado
            return redirect('remito_cargar_dias', remito_id=remito.id)
    else:
        form = RemitoForm()

    return render(request, 'remitos/remito_form.html', {'form': form})

@login_required
def remito_cargar_dias(request, remito_id):
    remito = Remito.objects.get(id=remito_id)
    dias = DiaServicio.objects.filter(remito=remito)

    if request.method == 'POST':
        for dia in dias:
            dia.horario = request.POST.get(f'horario_{dia.id}')
            dia.segundo_horario = request.POST.get(f'segundo_horario_{dia.id}')
            
            servicios_post = request.POST.get(f'servicios_{dia.id}')
            if servicios_post:
                dia.servicios = int(servicios_post)

            precio_post = request.POST.get(f'precio_{dia.id}')
            try:
                dia.precio = Decimal(precio_post)
            except (InvalidOperation, TypeError):
                dia.precio = Decimal('0.00')

            extra_post = request.POST.get(f'extra_{dia.id}')
            if extra_post:
                dia.extra = int(extra_post)

            precio_extra_post = request.POST.get(f'precio_extra_{dia.id}')
            try:
                dia.precio_extra = Decimal(precio_extra_post)
            except (InvalidOperation, TypeError):
                dia.precio_extra = Decimal('0.00')

            # Cálculo del importe, si corresponde:
            #dia.importe = (dia.precio or 0) * (dia.servicios or 0) + (dia.precio_extra or 0) * (dia.extra or 0)
            
            dia.save()
        
        return redirect('index')

    return render(request, 'remitos/cargar_dias.html', {
        'remito': remito,
        'dias': dias
    })

@login_required
def remito_detalle(request, pk):
    remito = get_object_or_404(Remito, pk=pk)
    dias_servicio = DiaServicio.objects.filter(remito=remito).order_by('dia')

    return render(request, 'remitos/remitoDetalle.html', {
        'remito': remito,
        'dias': dias_servicio
    })


@login_required
def remitos_por_empresa(request, empresa_id):
    empresa = Empresa.objects.get(pk=empresa_id)
    remitos = Remito.objects.filter(empresa=empresa)

    return render(request, 'remitos/remitos_por_empresa.html', {
        'empresa': empresa,
        'remitos': remitos
    })

"""
@login_required
def descargar_remito_pdf(request, pk):
    remito = Remito.objects.get(pk=pk)
    dias = DiaServicio.objects.filter(remito=remito)
    
    template = get_template('remitos/remito_pdf.html')
    html = template.render({'remito': remito, 'dias': dias})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="remito_{remito.id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    return response


@login_required
def generar_remito_pdf(request, remito_id):
    remito = Remito.objects.get(pk=remito_id)
    html_string = render_to_string('remito.html', {'remito': remito})
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="remito_{remito.id}.pdf"'
    return response
"""