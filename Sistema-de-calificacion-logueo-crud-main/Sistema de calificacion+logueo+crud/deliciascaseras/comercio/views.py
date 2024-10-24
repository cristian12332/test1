from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import Plato, Encuesta
from .forms import PlatoForm, EncuestaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required ,user_passes_test
from django.core.exceptions import PermissionDenied
from comercio.carrito import Carrito

# Creamos verificacion de usuario admin
def es_administrador(user):
    return user.is_staff
    
@login_required
def index(request):
    return render(request, 'index.html')

def logueo(request):
    return render(request, 'logueo.html')

def registro(request):
    if request.method == 'GET':
        return render(request, 'registro.html', {
        'form': UserCreationForm
        })
    
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], 
                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('iniciada')
            except IntegrityError:
                return  render(request, 'registro.html', {
                    'form': UserCreationForm,
                    "error": 'usuario ya existe'
                })
         
        return  render(request, 'registro.html', {
                    'form': UserCreationForm,
                    "error": 'password no coinciden'
                })
    
@login_required
def iniciada(request):
    return render(request, 'iniciada.html')


def logout_view(request):
    logout(request)
    return redirect(request.GET.get('next', '/'))


def iniciar_sesion(request):
    if request.method == 'GET':
            return render(request, 'iniciar.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])  

        if user is None:
          return render(request, 'iniciar.html', {
                'form': AuthenticationForm,
                'error': 'usuario o contraseña es incorrecto'
            })
        else:
            login(request, user)
            return redirect('iniciada')
        
def lista_de_platos(request):
    platos = Plato.objects.all()
    return render(request, 'comercio/lista_de_platos.html', {'platos': platos})

# vventas de platos.py

def pagina_venta(request):
    platos = Plato.objects.all()  # Obtener todos los platos
    carrito = Carrito(request)  # Obtener el carrito
    total_carrito = 0
    for item in carrito:
        if 'total' in item:
            total_carrito += item['total']

    if request.method == 'POST':
        form = EncuestaForm(request.POST)
        if form.is_valid():
            encuesta = form.save(commit=False)
            encuesta.plato = Plato.objects.get(id=request.POST['plato_id'])  # Asocia la encuesta con el plato
            encuesta.save()
            messages.success(request, 'Gracias por tu encuesta!')
            return redirect('pagina_venta')  # Redirige a la misma página
    else:
        form = EncuestaForm()

    return render(request, 'comercio/pagina_venta.html', {'platos': platos, 'form': form, 'carrito': carrito, 'total_carrito': total_carrito})

def editar_encuesta(request, encuesta_id):
    encuesta = get_object_or_404(Encuesta, id=encuesta_id)
    
    if request.method == "POST":
        form = EncuestaForm(request.POST, instance=encuesta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Encuesta actualizada con éxito.')
            return redirect('pagina_venta')  # Redirige a la página de venta o donde prefieras
    else:
        form = EncuestaForm(instance=encuesta)

    return render(request, 'comercio/encuesta_form.html', {'form': form})

def visualizacion_encuestas(request):
    platos = Plato.objects.all()
    resultados = []

    for plato in platos:
        encuestas = plato.encuestas.all()  # Obtiene todas las encuestas relacionadas
        if encuestas.exists():
            total_rating = sum(encuesta.rating for encuesta in encuestas)  # Suma las calificaciones
            cantidad_encuestas = encuestas.count()  # Cuenta el número de encuestas
            promedio_rating = total_rating / cantidad_encuestas  # Calcula el promedio
        else:
            total_rating = 0
            promedio_rating = 0
            cantidad_encuestas = 0

        resultados.append({
            'plato': plato,
            'total_rating': total_rating,
            'promedio_rating': promedio_rating,
            'cantidad_encuestas': cantidad_encuestas,
        })

    # Ordenar los resultados por promedio de calificación
    resultados.sort(key=lambda x: x['promedio_rating'], reverse=True)

    return render(request, 'visualizacion_encuestas.html', {'resultados': resultados})

def comprar_plato(request, plato_id):
    plato = get_object_or_404(Plato, id=plato_id)
    carrito = Carrito(request)
    carrito.agregar(plato)
    messages.success(request, f'Has añadido {plato.nombre} al carrito.')
    return redirect('pagina_venta')
#fin de la venta de los platos

@login_required
@permission_required('is_superuser')
def plato_list(request):
    if request.user.is_staff:
        platos = Plato.objects.all()
        return render(request, 'comercio/plato_list.html', {'platos': platos})
    return redirect('comercio/index')  # Redirigir si no es administrador

# CREAR PLATO:
@user_passes_test(es_administrador)
@login_required
def plato_create(request):
    if request.user.is_staff:
        if request.method == "POST":
            form = PlatoForm(request.POST, request.FILES)  # Asegúrate de incluir request.FILES
            if form.is_valid():
                form.save()
                return redirect('plato_list')
        else:
            form = PlatoForm()
        return render(request, 'comercio/plato_form.html', {'form': form})
    return redirect('index')  # Redirigir si no es administrador
#editar

@login_required
@permission_required('is_superuser')
def plato_update(request, pk):
    plato = get_object_or_404(Plato, pk=pk)
    if request.method == "POST":
        form = PlatoForm(request.POST, instance=plato)
        if form.is_valid():
            form.save()
            return redirect('plato_list')
    else:
        form = PlatoForm(instance=plato)
    return render(request, 'comercio/plato_form.html', {'form': form})
#editar fint

# Borrar plato
@login_required
@permission_required('is_superuser')
def plato_delete(request, pk):
    plato = get_object_or_404(Plato, pk=pk)
    if request.method == "POST":
        plato.delete()
        return redirect('plato_list')
    return render(request, 'comercio/plato_confirm_delete.html', {'plato': plato})

def ver_carrito(request):
    carrito = Carrito(request)
    total_carrito = 0
    for item in carrito:
        if 'total' in item:
            total_carrito += item['total']
    return render(request, 'comercio/ver_carrito.html', {
        'carrito': carrito,
        'total_carrito': total_carrito  # Pasamos el total al contexto
    })

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect('pagina_venta') 