from django.urls import path
from . import views
from .views import (
    plato_list,
    plato_create,
    plato_update,
    plato_delete,
    logueo,
    pagina_venta,
    comprar_plato,
    editar_encuesta,
    visualizacion_encuestas,
)

urlpatterns = [
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('plato_list/', plato_list, name='plato_list'),  # Ruta principal para listar platos
    path('nuevo/', plato_create, name='plato_create'),  # Ruta para crear un nuevo plato
    path('editar/<int:pk>/', plato_update, name='plato_update'),  # Ruta para editar un plato
    path('eliminar/<int:pk>/', plato_delete, name='plato_delete'),  # Ruta para eliminar un plato
    path('logueo/', views.logueo),  # Ruta para el logueo
    path('', pagina_venta, name='pagina_venta'),  # Ruta para la página de venta
    path('comprar/<int:plato_id>/', comprar_plato, name='comprar_plato'),  # Ruta para comprar un plato
    path('plato/listar/', plato_list, name='plato_list'),  # Ruta adicional para listar platos
    path('editar_encuesta/<int:encuesta_id>/', editar_encuesta, name='editar_encuesta'),  # Ruta para editar encuestas
    path('visualizar-encuestas/', visualizacion_encuestas, name='visualizar_encuestas'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('limpiar_carrito/', views.limpiar_carrito, name='limpiar_carrito'),
]