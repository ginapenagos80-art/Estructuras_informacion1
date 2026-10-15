import random

CONSUMO_MAX = 5000  # litros semanales maximos por familia

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
