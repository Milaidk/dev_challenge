from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm, LoginForm
from django.contrib import messages
from .forms import RutaForm
from .models import Ruta, Reserva, Usuario
from django.utils import timezone


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
            form.save()
            messages.success(request, "Ruta actualizada exitosamente.")
            return redirect('panel')
    else:
        form = RutaForm(instance=ruta)
        
    return render(request, 'editar_ruta.html', {'form': form, 'ruta': ruta})


@login_required
def panel_view(request):
    if request.user.tipo_usuario == 'conductor':
        rutas = Ruta.objects.filter(conductor=request.user)
        all_rutas = Ruta.objects.all().order_by('fecha', 'hora_salida')
        rutas_por_pagina = 1 
        paginator = Paginator(all_rutas, rutas_por_pagina)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
        'user': request.user,
        'rutas': page_obj,
        }
        
        return render(request, 'panel_conductor.html', context)
    else:
        # rutas = Ruta.objects.filter(fecha__gte=timezone.now().date(), asientos_disponibles__gt=0)
        all_rutas_disponibles = Ruta.objects.filter(
            fecha__gte=timezone.now().date(),
            asientos_disponibles__gt=0
        ).order_by('fecha', 'hora_salida')
        rutas_por_pagina = 1
        paginator = Paginator(all_rutas_disponibles, rutas_por_pagina)
        page_number = request.GET.get('page')
        rutas_page_obj = paginator.get_page(page_number)
        reservas_pasajero = Reserva.objects.filter(pasajero=request.user).order_by('-ruta__fecha', '-ruta__hora_salida')
        context = {
            'user': request.user,
            'rutas': rutas_page_obj,
            'reservas': reservas_pasajero, 
        }
        # reservas = Reserva.objects.filter(pasajero=request.user)
        return render(request, 'panel_pasajero.html', context)


@login_required
def publicar_ruta_view(request):
    if request.user.tipo_usuario != 'conductor':
        return redirect('panel')
    if request.method == 'POST':
        origen = request.POST.get('origen')
        sitio_llegada = request.POST.get('sitio_llegada', 'Universidad Católica del Ecuador')
        fecha = request.POST.get('fecha')
        hora_salida = request.POST.get('hora_salida')
        asientos = request.POST.get('asientos_disponibles')
        Ruta.objects.create(
            conductor=request.user,
            origen=origen,
            sitio_llegada=sitio_llegada,
            fecha=fecha,
            hora_salida=hora_salida,
            asientos_disponibles=asientos
        )
        return redirect('panel')
    return render(request, 'publicar_ruta.html')


@login_required
def reservar_ruta_view(request, ruta_id):
    ruta = Ruta.objects.get(id=ruta_id)
    if ruta.asientos_disponibles > 0 and not Reserva.objects.filter(ruta=ruta, pasajero=request.user).exists():
        Reserva.objects.create(ruta=ruta, pasajero=request.user)
        ruta.asientos_disponibles -= 1
        ruta.save()
    return redirect('panel')
