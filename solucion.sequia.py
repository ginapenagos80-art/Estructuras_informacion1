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
    def __init__(self, id, capacidad, nivel_actual=0):
        self.id, self.capacidad, self.nivel_actual = id, capacidad, nivel_actual

    def actualizar_nivel(self, nivel):
        if not 0 <= nivel <= self.capacidad:
            raise ValueError("El nivel debe estar entre 0 y la capacidad.")
        self.nivel_actual = nivel

    def estado_vacio(self):
        return self.nivel_actual == 0

class Familia:
    def __init__(self, id, numero_integrantes, consumo_semanal=0):
        self.id, self.numero_integrantes, self.consumo_semanal = id, numero_integrantes, consumo_semanal

    def registrar_consumo(self, litros):
        self.consumo_semanal = litros

    def consultar_consumo(self):
        return self.consumo_semanal

class Vereda:
    def __init__(self, nombre, municipio):
        self.nombre, self.municipio = nombre, municipio
        self.familias, self.tanques = [], []

    def agregar_familia(self, familia):
        self.familias.append(familia)

    def agregar_tanque(self, tanque):
        self.tanques.append(tanque)

    def consultar_reservas(self):
        return [t.nivel_actual for t in self.tanques]

from modelo import Pila, Tanque, Familia, Vereda

class CalculadoraReservas:
    def consumo_diarioT(self, familias):
        return sum(f.consultar_consumo() for f in familias) / 7

    def dias_agua(self, pila, diario, pendiente=None):
       
        pendiente = diario if pendiente is None else pendiente
        if pila.esta_vacia():                      
            return 0
        nivel = pila.desapilar()
        if nivel + 1e-9 >= pendiente:               
            pila.apilar(nivel - pendiente)
            return 1 + self.dias_agua(pila, diario)  
        return self.dias_agua(pila, diario, pendiente - nivel)  

def crear_vereda(nombre, municipio, niveles, n_familias, consumo_semanal):
   
    vereda = Vereda(nombre, municipio)
    for i, nivel in enumerate(niveles, start=1):
        tanque = Tanque(i, 30000)
        tanque.actualizar_nivel(nivel)
        vereda.agregar_tanque(tanque)
    for i in range(1, n_familias + 1):
        familia = Familia(i, 4)
        familia.registrar_consumo(consumo_semanal)
        vereda.agregar_familia(familia)
    return vereda

def calcular(vereda):
    calc = CalculadoraReservas()
    diario = calc.consumo_diarioT(vereda.familias)
    pila = Pila()
    for nivel in reversed(vereda.consultar_reservas()):
        pila.apilar(nivel)
    dias = calc.dias_agua(pila, diario)
    print(f"{vereda.nombre} ({vereda.municipio}) - consumo diario: {diario:,.0f} L")
    print(f"El agua alcanza para {dias} día(s)." if dias else "ALERTA: el agua no alcanza ni para un día.")

vereda1 = crear_vereda("La Concepción", "Quebradanegra", [25000], 40, 500)
vereda2 = crear_vereda("El Roble", "Guaduas", [10000, 5000, 5000], 40, 500)
vereda3 = crear_vereda("La Palma", "La Vega", [0], 40, 500)

for v in (vereda1, vereda2, vereda3):
    calcular(v)
