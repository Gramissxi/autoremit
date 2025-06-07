from django.contrib import admin
from .models import Remito, DiaServicio, Empresa

class DiaServicioInline(admin.TabularInline):
    model = DiaServicio
    extra = 0
    exclude = ('dia',)
    readonly_fields = ('dia', 'importe',)
    fields = (
        'horario', 'segundo_horario',
        'servicios', 'precio',
        'extra', 'precio_extra', 'total_extra',
        'importe',
    )


class RemitoAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'fecha_inicio', 'fecha_fin', 'importe_total')
    search_fields = ('empresa__nombre',)

    def get_inline_instances(self, request, obj=None):
        # Solo mostrar el inline si el Remito ya fue creado
        if obj:
            return [DiaServicioInline(self.model, self.admin_site)]
        return []

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Si es un nuevo Remito, generar los días automáticamente
        if not change:
            obj.generar_dias()

admin.site.register(Remito, RemitoAdmin)
admin.site.register(Empresa)
