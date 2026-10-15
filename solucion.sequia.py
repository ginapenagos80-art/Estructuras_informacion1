import random

CONSUMO_MAX = 5000  

class Pila:
    def __init__(self):
        self._elementos = []

    def apilar(self, x):
        self._elementos.append(x)

    def desapilar(self):
        return self._elementos.pop()

    def esta_vacia(self):
        return not self._elementos

class Tanque:
    def __init__(self, id_tanque, capacidad, nivel_actual=0):
        self.id = id_tanque
        self.capacidad = capacidad
        self.nivel_actual = nivel_actual

    def actualizar_nivel(self, nivel):
        if not 0 <= nivel <= self.capacidad:
            raise ValueError("El nivel debe estar entre 0 y la capacidad.")
        self.nivel_actual = nivel

class Familia:
    def __init__(self, id_familia, consumo_semanal=0):
        self.id = id_familia
        self.consumo_semanal = consumo_semanal

    def registrar_consumo(self, litros):
        if not (0 < litros <= CONSUMO_MAX):
            raise ValueError(f"El consumo debe estar entre 0 y {CONSUMO_MAX} litros.")
        self.consumo_semanal = litros

class Vereda:
    def __init__(self, nombre, municipio):
        self.nombre = nombre
        self.municipio = municipio
        self.familias = []
        self.tanques = []

class CalculadoraReservas:
    def consumo_diarioT(self, familias):
        diario = sum(f.consumo_semanal for f in familias) / 7
        if diario <= 0:
            raise ValueError("No hay consumo registrado: no se pueden calcular los días de reserva.")
        return diario

    def dias_agua(self, pila, diario, pendiente=None):
        pendiente = diario if pendiente is None else pendiente
        
        
        if pila.esta_vacia():
            return -1 if pendiente > 0 else 0
            
        nivel = pila.desapilar()
        if nivel + 1e-9 >= pendiente:
            pila.apilar(nivel - pendiente)
            siguiente = self.dias_agua(pila, diario)
            return 1 + (siguiente if siguiente != -1 else 0)
        
        return self.dias_agua(pila, diario, pendiente - nivel)


def crear_vereda(nombre, municipio, niveles, n_familias=40):
    vereda = Vereda(nombre, municipio)
    
    for i, nivel in enumerate(niveles, start=1):
        tanque = Tanque(i, 30000)
        tanque.actualizar_nivel(nivel)
        vereda.tanques.append(tanque)
        
    for i in range(1, n_familias + 1):
        familia = Familia(i)
        familia.registrar_consumo(random.randint(100, 1000))
        vereda.familias.append(familia)
        
    return vereda

def calcular(vereda):
    calc = CalculadoraReservas()
    try:
        diario = calc.consumo_diarioT(vereda.familias)
        pila = Pila()
        for tanque in reversed(vereda.tanques):
            pila.apilar(tanque.nivel_actual)
            
        dias = calc.dias_agua(pila, diario)
        
        print(f"\n{vereda.nombre} ({vereda.municipio})")
        print(f"Consumo diario total: {diario:,.0f} L")
        
        if dias <= 0:
            print("ALERTA: ¡Se ha agotado el agua! Las reservas no alcanzan ni para 1 día completo.")
        else:
            print(f"El agua alcanza para {dias} día(s) completos.")
            print("ALERTA: ¡Se ha agotado el agua! Ya no hay suficientes reservas para los días siguientes.")

    except (ValueError, RecursionError) as e:
        print(f"Error en {vereda.nombre}: {e}")


for nombre, municipio, niveles in [
    ("La Concepción", "Quebradanegra", [25000]),
    ("El Roble", "Guaduas", [10000, 5000, 5000]),
    ("La Palma", "La Vega", [0])
]:
    calcular(crear_vereda(nombre, municipio, niveles))
