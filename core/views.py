import os
import json
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm, LoginForm
from django.contrib import messages
from .forms import RutaForm
from .models import Ruta, Reserva, Usuario
from .models import Mensaje
from django.utils import timezone
from django.http import JsonResponse
from datetime import date
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages


ruta_json = os.path.join(settings.BASE_DIR, 'core', 'sectores_quito.json')
with open(ruta_json, 'r', encoding='utf-8') as f:
    sectores_quito = json.load(f)

# uso de api para rutas
def api_rutas_sector(request):
    sector = request.GET.get('sector', '').upper()
    resultados = []
    for item in sectores_quito:
        if sector in item['nombre']:
            resultados.append(item)
            
            
    if resultados:
        return JsonResponse({'sectores': resultados})
    return JsonResponse({'sectores': []})

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('panel')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('panel')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})



#mesajes comunidad puce
@login_required
def enviar_mensaje_view(request):
    if request.method == 'POST':
        contenido = request.POST.get('mensaje')
        tipo_destinatario = request.POST.get('destinatario_tipo')
        emisor = request.user

        if tipo_destinatario not in ['conductor', 'pasajero']:
            messages.error(request, "Tipo de destinatario no válido.")
            return redirect('panel')

        # Evita que el mensaje se envíe a uno mismo
        receptores = Usuario.objects.filter(tipo_usuario=tipo_destinatario).exclude(id=emisor.id)

        for receptor in receptores:
            Mensaje.objects.create(emisor=emisor, receptor=receptor, contenido=contenido)

        messages.success(request, f"Mensaje enviado a {tipo_destinatario}s.")

    return redirect('panel')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def editar_ruta_view(request, ruta_id):
    try:
        ruta = Ruta.objects.get(id=ruta_id, conductor=request.user)
    except Ruta.DoesNotExist:
        messages.error(request, "La ruta no existe o no te pertenece.")
        return redirect('panel')
    
    if request.method == 'POST':
        form = RutaForm(request.POST, instance=ruta)
        if form.is_valid():
            ruta_editada = form.save(commit=False)
            ruta_editada.sitio_llegada = "PONTIFICIA UNIVERSIDAD CATOLICA DEL ECUADOR" #CAMPO UNICOS
            ruta_editada.save()
            messages.success(request, "Ruta actualizada exitosamente.")
            return redirect('panel')
    else:
        form = RutaForm(instance=ruta)
        
    return render(request, 'editar_ruta.html', {'form': form, 'ruta': ruta})


@login_required
def eliminar_ruta_view(request, ruta_id):
    if request.method == 'POST':
        ruta = get_object_or_404(Ruta, id=ruta_id, conductor=request.user)
        ruta.delete()
        messages.success(request, "Ruta eliminada exitosamente.")
        return redirect('panel')
    return render(request, 'confirmar_eliminacion.html', {'ruta': ruta})


@login_required
def panel_view(request):
    if request.user.tipo_usuario == 'conductor':
        rutas_conductor = Ruta.objects.filter(conductor=request.user).order_by('fecha', 'hora_salida')
        # all_rutas = Ruta.objects.all().order_by('fecha', 'hora_salida')
        rutas_por_pagina = 1 
        paginator = Paginator(rutas_conductor, rutas_por_pagina)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        mensajes = Mensaje.objects.filter(
            receptor__tipo_usuario=request.user.tipo_usuario
        ).order_by('-timestamp')[:10]
        
        context = {
        'user': request.user,
        'rutas': page_obj,
        'mensajes': mensajes,
        }
        
        return render(request, 'panel_conductor.html', context)
    else:
        sector_pasajero = request.user.origen.upper()
        sectores_cercanos = set()

        for item in sectores_quito:
            nombre = item['nombre'].upper()
            barrios = [b.upper() for b in item['barriosCercanos']]

            if sector_pasajero == nombre or sector_pasajero in barrios:
                sectores_cercanos.add(nombre)
                sectores_cercanos.update(barrios)

        sectores_cercanos = list(sectores_cercanos)
        rutas_cercanas = Ruta.objects.filter(
            origen__in=sectores_cercanos,
            fecha__gte=timezone.now().date(),
            asientos_disponibles__gt=0
        ).order_by('fecha', 'hora_salida')

        rutas_por_pagina = 1
        paginator = Paginator(rutas_cercanas, rutas_por_pagina)
        page_number = request.GET.get('page')
        rutas_page_obj = paginator.get_page(page_number)

        reservas_pasajero = Reserva.objects.filter(
            pasajero=request.user
        ).order_by('-ruta__fecha', '-ruta__hora_salida')
        
   
        mensajes = Mensaje.objects.filter(
            receptor__tipo_usuario=request.user.tipo_usuario
        ).order_by('-timestamp')[:10]

        context = {
            'user': request.user,
            'rutas': rutas_page_obj,
            'reservas': reservas_pasajero,
            'mensajes': mensajes,
            
        }

        return render(request, 'panel_pasajero.html', context)


@login_required
def publicar_ruta_view(request):
    if request.user.tipo_usuario != 'conductor':
        return redirect('panel')
    if request.method == 'POST':
        origen = request.POST.get('origen')
        sitio_llegada = "PONTIFICIA UNIVERSIDAD CATOLICA DEL ECUADOR"
        fecha = request.POST.get('fecha')
        hora_salida = request.POST.get('hora_salida')
        asientos = request.POST.get('asientos_disponibles')
        
        if fecha < str(date.today()):
            messages.error(request, "La fecha no puede ser anterior a hoy.")
            return redirect('panel')
        
        Ruta.objects.create(
            conductor=request.user,
            origen=origen,
            sitio_llegada=sitio_llegada,
            fecha=fecha,
            hora_salida=hora_salida,
            asientos_disponibles=asientos
        )
        return redirect('panel')
    return render(request, 'publicar_ruta.html', {'today': date.today().isoformat()})





@login_required
def reservar_ruta_view(request, ruta_id):
    ruta = Ruta.objects.get(id=ruta_id)
    if ruta.asientos_disponibles > 0 and not Reserva.objects.filter(ruta=ruta, pasajero=request.user).exists():
        Reserva.objects.create(ruta=ruta, pasajero=request.user)
        ruta.asientos_disponibles -= 1
        ruta.save()
    return redirect('panel')
