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