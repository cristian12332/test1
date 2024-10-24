from decimal import Decimal
from .models import Plato

class Carrito:
    def __init__(self, request):
        self.session = request.session
        carrito = self.session.get('carrito')
        if not carrito:
            carrito = self.session['carrito'] = {}
        self.carrito = carrito

    def agregar(self, plato):
        plato_id = str(plato.id)
        if plato_id not in self.carrito:
            self.carrito[plato_id] = {
                'cantidad': 1,
                'precio': str(plato.precio)
            }
        else:
            self.carrito[plato_id]['cantidad'] += 1
        self.guardar()

    def guardar(self):
        self.session.modified = True

    def __iter__(self):
        platos_ids = self.carrito.keys()
        platos = Plato.objects.filter(id__in=platos_ids)
        
        # Iteramos sobre los platos y asignamos sus valores al carrito
        for plato in platos:
            self.carrito[str(plato.id)]['plato'] = plato
            self.carrito[str(plato.id)]['precio'] = plato.precio
            
        # Iteramos sobre los elementos del carrito y devolvemos cada uno
        for item in self.carrito.values():
            if 'precio' in item:
                item['total'] = item['precio'] * item['cantidad']
            yield item

    def eliminar(self, plato):
        plato_id = str(plato.id)
        if plato_id in self.carrito:
            del self.carrito[plato_id]
            self.guardar()

    def limpiar(self):
        self.session['carrito'] = {}
        self.guardar()

def obtener_total(self):
    total = 0
    for item in self.carrito.values():
        if 'precio' in item:
            total += Decimal(item['precio']) * item['cantidad']
        else:
            # Si la clave 'precio' no existe, puedes agregar un mensaje de error o una acción por defecto
            print("Error: La clave 'precio' no existe en el diccionario")
    return total