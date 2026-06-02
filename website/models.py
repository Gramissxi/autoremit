from django.db import models


class Consulta(models.Model):

    nombre = models.CharField(max_length=100)

    empresa = models.CharField(
        max_length=100,
        blank=True
    )

    telefono = models.CharField(max_length=30)

    mensaje = models.TextField()

    fecha = models.DateTimeField(auto_now_add=True)

    estado = models.CharField(
        max_length=30,
        default='Pendiente'
    )

    def __str__(self):
        return self.nombre