from django.db import models
from datetime import timedelta

class Empresa(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False, unique=True)
 
    def __str__(self):
        return self.nombre
    

class Remito(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    importe_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def generar_dias(self):
        if self.dias.exists():
            return

        dias_semana_es = {
            'Monday': 'Lunes',
            'Tuesday': 'Martes',
            'Wednesday': 'Miércoles',
            'Thursday': 'Jueves',
            'Friday': 'Viernes',
            'Saturday': 'Sábado',
            'Sunday': 'Domingo'
        }

        fecha_actual = self.fecha_inicio
        while fecha_actual <= self.fecha_fin:
            nombre_dia = fecha_actual.strftime('%A')
            DiaServicio.objects.create(
                remito=self,
                dia=f"{fecha_actual.strftime('%d/%m/%Y')} {dias_semana_es[nombre_dia]} ",  # Ej: Lunes 10/06/2024
                servicios=1,
                precio=0,
                extra=0,
                precio_extra=0,
                importe=0
            )
            fecha_actual += timedelta(days=1)

        self.actualizar_importe_total()

    def actualizar_importe_total(self):
        total = sum(
        d.importe or 0  # ✅ Ya incluye total_extra si corresponde
        for d in self.dias.all()
        )
        self.importe_total = total
        super().save(update_fields=['importe_total'])


    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new or not self.dias.exists():
            if self.fecha_inicio and self.fecha_fin:
                self.generar_dias()
        else:
            self.actualizar_importe_total()

    def __str__(self):
        return f"Remito de {self.empresa} del {self.fecha_inicio} al {self.fecha_fin}"


class DiaServicio(models.Model):
    TURNOS_CHOICES = [
        ("12:00 hs a 18:00 hs", "12:00 hs a 18:00 hs"),
        ("19:00 hs a 01:00 hs", "19:00 hs a 01:00 hs")
    ]
    CANTIDAD_SERVICIOS = [
        (1, "1 servicio"),
        (2, "2 servicios"),
        (3, "3 servicios"),
        (4, "4 servicios"),
    ]
    
    dia = models.CharField(max_length=15, editable=False)  # No editable

    remito = models.ForeignKey(Remito, on_delete=models.CASCADE, related_name='dias')
    
    horario = models.CharField(max_length=50, choices=TURNOS_CHOICES, blank=True, null=True)
    segundo_horario = models.CharField(max_length=50, choices=TURNOS_CHOICES, blank=True, null=True)
    servicios = models.IntegerField(choices=CANTIDAD_SERVICIOS)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    extra = models.IntegerField(choices=CANTIDAD_SERVICIOS, null=True, blank=True)
    precio_extra = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_extra = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    importe = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    fecha = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
    # Calcular importe base
        if self.precio and self.servicios:
            self.importe = self.precio * self.servicios
        else:
            self.importe = 0

    # Calcular total extra si el usuario lo completó
        if self.extra and self.precio_extra:
            self.total_extra = self.extra * self.precio_extra
            self.importe += self.total_extra
        else:
            self.total_extra = 0

        super().save(*args, **kwargs)
        self.remito.actualizar_importe_total()


    def __str__(self):
        return f"{self.dia} - {self.servicios} servicios - ${self.importe}"
