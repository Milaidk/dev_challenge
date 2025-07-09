from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm, LoginForm
from django.contrib import messages
from .forms import RutaForm
from .models import Ruta, Reserva, Usuario
from django.utils import timezone
from django.http import JsonResponse
from datetime import date

sectores_quito = [
    {
        "nombre": "ALANGASÍ",
        "barriosCercanos": ["VALLE DE LOS CHILLOS"]
    },
    {
        "nombre": "ALOASÍ",
        "barriosCercanos": ["MACHACHI"]
    },
    {
        "nombre": "AMAGUAÑA",
        "barriosCercanos": ["VALLE DE LOS CHILLOS"]
    },
    {
        "nombre": "AMARU ÑAN",
        "barriosCercanos": ["PUENGASÍ"]
    },
    {
        "nombre": "BATÁN",
        "barriosCercanos": ["UNIVERSIDAD DE LAS AMÉRICAS (UDLA)"]
    },
    {
        "nombre": "BATÁN ALTO",
        "barriosCercanos": ["UDLA"]
    },
    {
        "nombre": "BELLAVISTA",
        "barriosCercanos": ["UDLA", "LA FLORESTA", "LA CAROLINA", "LA MARISCAL", "GUÁPULO", "UNIVERSIDAD DE LAS AMÉRICAS (UDLA)"]
    },
    {
        "nombre": "CALACALÍ",
        "barriosCercanos": ["SAN ANTONIO DE PICHINCHA"]
    },
    {
        "nombre": "CALDERÓN",
        "barriosCercanos": ["LLANO CHICO", "PONCEANO", "COTOCOLLAO", "UNIVERSIDAD INTERNACIONAL SEK", "CARCELÉN"]
    },
    {
        "nombre": "CARCELÉN",
        "barriosCercanos": ["COTOCOLLAO", "PONCEANO", "EL CONDADO", "UNIVERSIDAD INTERNACIONAL SEK", "CALDERÓN"]
    },
    {
        "nombre": "CAROLINA",
        "barriosCercanos": ["UDLA", "UNIVERSIDAD DE LAS AMÉRICAS (UDLA)"]
    },
    {
        "nombre": "CAUPICHU",
        "barriosCercanos": ["PUENGASÍ"]
    },
    {
        "nombre": "CENTRO HISTÓRICO",
        "barriosCercanos": ["SAN ROQUE", "LA LIBERTAD", "EL TEJAR", "ITCHIMBÍA", "SAN BLAS", "LA LOMA"]
    },
    {
        "nombre": "CHILIBULO",
        "barriosCercanos": ["EL CALZADO", "LA MAGDALENA", "LLOA"]
    },
    {
        "nombre": "CHILLOGALLO",
        "barriosCercanos": ["EL CONDADO", "TURUBAMBA", "LA ECUATORIANA", "LA MERCED", "QUITUMBE"]
    },
    {
        "nombre": "CHIMBACALLE",
        "barriosCercanos": ["SOLANDA", "RECREO", "LA MAGDALENA", "SAN BARTOLO", "FERROVIARIA", "VILLAFLORA"]
    },
    {
        "nombre": "COMITÉ DEL PUEBLO",
        "barriosCercanos": ["PONCEANO"]
    },
    {
        "nombre": "CONOCOTO",
        "barriosCercanos": ["ESPOCH EXTENSIÓN", "VALLE DE LOS CHILLOS", "SAN RAFAEL"]
    },
    {
        "nombre": "COTOCOLLAO",
        "barriosCercanos": ["PONCEANO", "EL BOSQUE", "SAN ISIDRO DEL INCA", "CARCELÉN", "CALDERÓN", "EL CONDADO"]
    },
    {
        "nombre": "COTOCALLAO ALTO",
        "barriosCercanos": ["CARCELÉN"]
    },
    {
        "nombre": "CUMBAYÁ",
        "barriosCercanos": ["GUÁPULO", "TUMBACO", "USFQ", "VALLE DE LOS CHILLOS", "LA TEIBA", "LOS ALMENDROS", "SAN JUAN DE CUMBAYÁ"]
    },
    {
        "nombre": "EL BELÉN",
        "barriosCercanos": ["UNIVERSIDAD CENTRAL", "UNIVERSIDAD TECNOLÓGICA EQUINOCCIAL (UTE)"]
    },
    {
        "nombre": "EL BOSQUE",
        "barriosCercanos": ["COTOCOLLAO"]
    },
    {
        "nombre": "EL BUEY",
        "barriosCercanos": ["MACHACHI"]
    },
    {
        "nombre": "EL CALZADO",
        "barriosCercanos": ["SOLANDA", "RECREO", "LA MAGDALENA", "CHILIBULO"]
    },
    {
        "nombre": "EL CAMAL",
        "barriosCercanos": ["FERROVIARIA"]
    },
    {
        "nombre": "EL CONDADO",
        "barriosCercanos": ["COTOCOLLAO", "PONCEANO", "LA ROLDÓS", "PISULÍ", "CARCELÉN", "CHILLOGALLO", "UNIVERSIDAD INTERNACIONAL SEK"]
    },
    {
        "nombre": "EL EJIDO",
        "barriosCercanos": ["PUCE", "LA FLORESTA", "UNIVERSIDAD CENTRAL", "UCE", "LA MARISCAL", "PONTIFICIA UNIVERSIDAD CATOLICA DEL ECUADOR"]
    },
    {
        "nombre": "EL GIRÓN",
        "barriosCercanos": ["UNIVERSIDAD POLITÉCNICA SALESIANA"]
    },
    {
        "nombre": "EL QUINCHE",
        "barriosCercanos": ["TUMBACO"]
    },
    {
        "nombre": "EL TEJAR",
        "barriosCercanos": ["CENTRO HISTÓRICO"]
    },
    {
        "nombre": "EL TROJE",
        "barriosCercanos": ["QUITUMBE"]
    },
    {
        "nombre": "ESPE",
        "barriosCercanos": ["VALLE DE LOS CHILLOS", "SANGOLQUÍ", "ESPOCH EXTENSIÓN", "SAN RAFAEL"]
    },
    {
        "nombre": "ESPOCH EXTENSIÓN",
        "barriosCercanos": ["SANGOLQUÍ", "CONOCOTO", "ESPE"]
    },
    {
        "nombre": "FERROVIARIA",
        "barriosCercanos": ["CHIMBACALLE", "FERROVIARIA BAJA", "EL CAMAL", "LA MAGDALENA", "LA ARGELIA"]
    },
    {
        "nombre": "FERROVIARIA BAJA",
        "barriosCercanos": ["FERROVIARIA"]
    },
    {
        "nombre": "GONZÁLEZ SUÁREZ",
        "barriosCercanos": ["LA CAROLINA"]
    },
    {
        "nombre": "GRANDA CENTENO",
        "barriosCercanos": ["UDLA"]
    },
    {
        "nombre": "GUAMANÍ",
        "barriosCercanos": ["QUITUMBE", "TURUBAMBA", "LA COCHA", "SANTO TOMÁS", "LA ARAGÓN"]
    },
    {
        "nombre": "GUÁPULO",
        "barriosCercanos": ["BELLAVISTA", "LA FLORESTA", "SAN FRANCISCO DE GUÁPULO", "TOTORAS", "LLOA", "CUMBAYÁ"]
    },
    {
        "nombre": "IÑAQUITO",
        "barriosCercanos": ["LA PAZ", "LA CAROLINA", "JIPILAPA", "MARISCAL SUCRE", "RUMIPAMBA", "LA MARISCAL"]
    },
    {
        "nombre": "ITCHIMBÍA",
        "barriosCercanos": ["CENTRO HISTÓRICO", "PUENGASÍ"]
    },
    {
        "nombre": "JIPILAPA",
        "barriosCercanos": ["IÑAQUITO"]
    },
    {
        "nombre": "LA ARAGÓN",
        "barriosCercanos": ["GUAMANÍ"]
    },
    {
        "nombre": "LA ARGELIA",
        "barriosCercanos": ["LLOA", "FERROVIARIA"]
    },
    {
        "nombre": "LA CAROLINA",
        "barriosCercanos": ["BELLAVISTA", "IÑAQUITO", "LA PRADERA", "QUITO TENIS", "GONZÁLEZ SUÁREZ", "LA MARISCAL"]
    },
    {
        "nombre": "LA COCHA",
        "barriosCercanos": ["GUAMANÍ"]
    },
    {
        "nombre": "LA ECUATORIANA",
        "barriosCercanos": ["QUITUMBE", "TURUBAMBA", "CHILLOGALLO"]
    },
    {
        "nombre": "LA FLORESTA",
        "barriosCercanos": ["BELLAVISTA", "EL EJIDO", "LA PAZ", "LA MARISCAL", "GUÁPULO"]
    },
    {
        "nombre": "LA LIBERTAD",
        "barriosCercanos": ["CENTRO HISTÓRICO", "PUENGASÍ"]
    },
    {
        "nombre": "LA LOMA",
        "barriosCercanos": ["CENTRO HISTÓRICO"]
    },
    {
        "nombre": "LA MAGDALENA",
        "barriosCercanos": ["EL CALZADO", "SOLANDA", "RECREO", "CHIMBACALLE", "CHILIBULO", "FERROVIARIA", "UNIVERSIDAD POLITÉCNICA SALESIANA"]
    },
    {
        "nombre": "LA MARISCAL",
        "barriosCercanos": ["EL EJIDO", "LA FLORESTA", "BELLAVISTA", "RUMIPAMBA", "IÑAQUITO", "LA CAROLINA", "PUCE", "PONTIFICIA UNIVERSIDAD CATOLICA DEL ECUADOR", "UCE"]
    },
    {
        "nombre": "LA MERCED",
        "barriosCercanos": ["CHILLOGALLO"]
    },
    {
        "nombre": "LA MITAD DEL MUNDO",
        "barriosCercanos": ["SAN ANTONIO DE PICHINCHA"]
    },
    {
        "nombre": "LA MORITA",
        "barriosCercanos": ["TUMBACO"]
    },
    {
        "nombre": "LA PAZ",
        "barriosCercanos": ["LA FLORESTA", "IÑAQUITO"]
    },
    {
        "nombre": "LA PRADERA",
        "barriosCercanos": ["LA CAROLINA"]
    },
    {
        "nombre": "LA ROLDÓS",
        "barriosCercanos": ["EL CONDADO"]
    },
    {
        "nombre": "LA TEIBA",
        "barriosCercanos": ["CUMBAYÁ"]
    },
    {
        "nombre": "LA VALLE",
        "barriosCercanos": ["VILLAFLORA"]
    },
    {
        "nombre": "LLANO CHICO",
        "barriosCercanos": ["CALDERÓN"]
    },
    {
        "nombre": "LLOA",
        "barriosCercanos": ["CHILIBULO", "LA ARGELIA", "GUAPULO"]
    },
    {
        "nombre": "LOS ALMENDROS",
        "barriosCercanos": ["CUMBAYÁ"]
    },
    {
        "nombre": "MACHACHI",
        "barriosCercanos": ["ALOASÍ", "EL BUEY", "PAJÁN", "UYUMBICHO"]
    },
    {
        "nombre": "MARISCAL SUCRE",
        "barriosCercanos": ["IÑAQUITO"]
    },
    {
        "nombre": "MIRAFLORES",
        "barriosCercanos": ["UNIVERSIDAD TECNOLÓGICA EQUINOCCIAL (UTE)"]
    },
    {
        "nombre": "OYACACHI",
        "barriosCercanos": ["CALDERÓN"]
    },
    {
        "nombre": "PAJÁN",
        "barriosCercanos": ["MACHACHI"]
    },
    {
        "nombre": "PIFO",
        "barriosCercanos": ["TUMBACO"]
    },
    {
        "nombre": "PÍNTAG",
        "barriosCercanos": ["VALLE DE LOS CHILLOS"]
    },
    {
        "nombre": "PISULÍ",
        "barriosCercanos": ["EL CONDADO"]
    },
    {
        "nombre": "PONCEANO",
        "barriosCercanos": ["EL CONDADO", "COTOCOLLAO", "COMITÉ DEL PUEBLO", "CARCELÉN", "CALDERÓN"]
    },
    {
        "nombre": "PONTIFICIA UNIVERSIDAD CATOLICA DEL ECUADOR",
        "barriosCercanos": ["LA MARISCAL", "EL EJIDO", "UNIVERSIDAD CENTRAL"]
    },
    {
        "nombre": "PUCE",
        "barriosCercanos": ["LA MARISCAL", "EL EJIDO", "UNIVERSIDAD CENTRAL"]
    },
    {
        "nombre": "PUELIMBÍ",
        "barriosCercanos": ["SAN ANTONIO DE PICHINCHA"]
    },
    {
        "nombre": "PUEMBO",
        "barriosCercanos": ["TUMBACO", "USFQ"]
    },
    {
        "nombre": "PUENGASÍ",
        "barriosCercanos": ["ITCHIMBÍA", "LA LIBERTAD", "SAN ISIDRO", "CAUPICHU", "AMARU ÑAN"]
    },
    {
        "nombre": "QUITO SUR",
        "barriosCercanos": ["VILLAFLORA"]
    },
    {
        "nombre": "QUITO TENIS",
        "barriosCercanos": ["LA CAROLINA"]
    },
    {
        "nombre": "QUITUMBE",
        "barriosCercanos": ["GUAMANÍ", "TURUBAMBA", "SOLANDA", "EL TROJE", "LA ECUATORIANA", "CHILLOGALLO"]
    },
    {
        "nombre": "RECREO",
        "barriosCercanos": ["SOLANDA", "LA MAGDALENA", "EL CALZADO", "VILLAFLORA", "SAN BARTOLO", "CHIMBACALLE", "UNIVERSIDAD POLITÉCNICA SALESIANA"]
    },
    {
        "nombre": "RUMIPAMBA",
        "barriosCercanos": ["LA MARISCAL", "IÑAQUITO"]
    },
    {
        "nombre": "SAN ANTONIO DE PICHINCHA",
        "barriosCercanos": ["LA MITAD DEL MUNDO", "PUELIMBÍ", "CALACALÍ"]
    },
    {
        "nombre": "SAN BARTOLO",
        "barriosCercanos": ["CHIMBACALLE", "SOLANDA", "RECREO", "VILLAFLORA"]
    },
    {
        "nombre": "SAN BLAS",
        "barriosCercanos": ["CENTRO HISTÓRICO"]
    },
    {
        "nombre": "SAN FRANCISCO DE GUÁPULO",
        "barriosCercanos": ["GUÁPULO"]
    },
    {
        "nombre": "SAN ISIDRO",
        "barriosCercanos": ["PUENGASÍ"]
    },
    {
        "nombre": "SAN ISIDRO DEL INCA",
        "barriosCercanos": ["COTOCOLLAO"]
    },
    {
        "nombre": "SAN JUAN",
        "barriosCercanos": ["UNIVERSIDAD CENTRAL", "UNIVERSIDAD TECNOLÓGICA EQUINOCCIAL (UTE)"]
    },
    {
        "nombre": "SAN JUAN DE CUMBAYÁ",
        "barriosCercanos": ["CUMBAYÁ"]
    },
    {
        "nombre": "SAN RAFAEL",
        "barriosCercanos": ["ESPE", "VALLE DE LOS CHILLOS"]
    },
    {
        "nombre": "SAN ROQUE",
        "barriosCercanos": ["CENTRO HISTÓRICO"]
    },
    {
        "nombre": "SANTO TOMÁS",
        "barriosCercanos": ["GUAMANÍ"]
    },
    {
        "nombre": "SANGOLQUÍ",
        "barriosCercanos": ["ESPE", "ESPOCH EXTENSIÓN"]
    },
    {
        "nombre": "SOLANDA",
        "barriosCercanos": ["RECREO", "LA MAGDALENA", "CHIMBACALLE", "EL CALZADO", "SAN BARTOLO", "QUITUMBE"]
    },
    {
        "nombre": "TOTORAS",
        "barriosCercanos": ["GUÁPULO"]
    },
    {
        "nombre": "TUMBACO",
        "barriosCercanos": ["CUMBAYÁ", "PUEMBO", "PIFO", "LA MORITA", "EL QUINCHE", "USFQ"]
    },
    {
        "nombre": "TURUBAMBA",
        "barriosCercanos": ["QUITUMBE", "GUAMANÍ", "CHILLOGALLO", "LA ECUATORIANA"]
    },
    {
        "nombre": "UCE",
        "barriosCercanos": ["LA MARISCAL", "EL EJIDO", "UNIVERSIDAD CENTRAL"]
    },
    {
        "nombre": "UDLA",
        "barriosCercanos": ["GRANDA CENTENO", "BATÁN ALTO", "BELLAVISTA", "CAROLINA"]
    },
    {
        "nombre": "UNIVERSIDAD CENTRAL",
        "barriosCercanos": ["PUCE", "EL BELÉN", "SAN JUAN", "EL EJIDO", "PONTIFICIA UNIVERSIDAD CATOLICA DEL ECUADOR", "UCE"]
    },
    {
        "nombre": "UNIVERSIDAD DE LAS AMÉRICAS (UDLA)",
        "barriosCercanos": ["BATÁN", "BELLAVISTA", "CAROLINA"]
    },
    {
        "nombre": "UNIVERSIDAD INTERNACIONAL SEK",
        "barriosCercanos": ["CALDERÓN", "CARCELÉN", "EL CONDADO"]
    },
    {
        "nombre": "UNIVERSIDAD POLITÉCNICA SALESIANA",
        "barriosCercanos": ["EL GIRÓN", "RECREO", "LA MAGDALENA"]
    },
    {
        "nombre": "UNIVERSIDAD TECNOLÓGICA EQUINOCCIAL (UTE)",
        "barriosCercanos": ["MIRAFLORES", "EL BELÉN", "SAN JUAN"]
    },
    {
        "nombre": "USFQ",
        "barriosCercanos": ["CUMBAYÁ", "TUMBACO", "PUEMBO"]
    },
    {
        "nombre": "UYUMBICHO",
        "barriosCercanos": ["MACHACHI"]
    },
    {
        "nombre": "VALLE DE LOS CHILLOS",
        "barriosCercanos": ["CONOCOTO", "SAN RAFAEL", "CUMBAYÁ", "ALANGASÍ", "AMAGUAÑA", "PÍNTAG", "ESPE"]
    },
    {
        "nombre": "VILLAFLORA",
        "barriosCercanos": ["RECREO", "QUITO SUR", "LA VALLE", "CHIMBACALLE", "SAN BARTOLO"]
    }
]


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
        sector_pasajero = request.user.origen.upper()
        sectores_cercanos = []

        for item in sectores_quito:
            if sector_pasajero == item['nombre'] or sector_pasajero in item['barriosCercanos']:
                sectores_cercanos = [item['nombre']] + item['barriosCercanos']
                break
        # rutas = Ruta.objects.filter(fecha__gte=timezone.now().date(), asientos_disponibles__gt=0)
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

        context = {
            'user': request.user,
            'rutas': rutas_page_obj,
            'reservas': reservas_pasajero,
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
