from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class Usuario(AbstractUser):
    nombre_completo = models.CharField(max_length=100)
    origen = models.CharField(max_length=100) 
    correo_institucional = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    facultad = models.CharField(max_length=100)
    TIPO_USUARIO_CHOICES = [
        ('conductor', 'Conductor'),
        ('pasajero', 'Pasajero'),
    ]
    tipo_usuario = models.CharField(max_length=10, choices=TIPO_USUARIO_CHOICES)

    USERNAME_FIELD = 'correo_institucional'
    REQUIRED_FIELDS = ['username', 'nombre_completo', 'telefono', 'facultad', 'tipo_usuario', 'origen']

    def __str__(self):
        return self.nombre_completo.capitalize()

class Ruta(models.Model):
    conductor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='rutas')
    origen = models.CharField(max_length=200)
    hora_salida = models.TimeField()
    fecha = models.DateField()
    sitio_llegada = models.CharField(max_length=200, default='Universidad Católica del Ecuador')
    asientos_disponibles = models.PositiveIntegerField(default=4)

    def __str__(self):
        return f"{self.origen} → {self.sitio_llegada} ({self.fecha} {self.hora_salida})"

class Reserva(models.Model):
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE, related_name='reservas')
    pasajero = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='reservas')
    fecha_reserva = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reserva de {self.pasajero} en {self.ruta}"
    

class Mensaje(models.Model):
    emisor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mensajes_enviados')
    receptor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mensajes_recibidos')
    contenido = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.emisor} ➜ {self.receptor}: {self.contenido[:20]}"

