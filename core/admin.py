from django.contrib import admin
from .models import Usuario, Ruta, Reserva
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(Usuario, UserAdmin)
admin.site.register(Ruta)
admin.site.register(Reserva)
