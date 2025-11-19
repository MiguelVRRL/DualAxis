import math
from collections import Counter

class MedidasResumen:
    def __init__(self, x: list[int | float], fr: list[int] = []):
        """
        x: valores
        fr: frecuencias (vacía => datos simples)
        """
        if not x:
            raise ValueError("La lista de valores x no puede estar vacía.")

        self.x = x
        self.fr = fr if fr else [1] * len(x)  # si no hay frecuencia = 1 por dato

        if len(self.x) != len(self.fr):
            raise ValueError("x y fr deben tener la misma longitud.")

        # Construir lista expandida para cálculos exactos
        self.lista = []
        for valor, freq in zip(self.x, self.fr):
            self.lista += [valor] * freq

        self.lista.sort()
        self.n = len(self.lista)

    # -------------------------------------------------------
    # MÉTODOS ESTADÍSTICOS
    # -------------------------------------------------------
    def media(self):
        return sum(self.lista) / self.n

    def promedio(self):
        return self.media()

    def mediana(self):
        mid = self.n // 2
        if self.n % 2 == 0:
            return (self.lista[mid - 1] + self.lista[mid]) / 2
        return self.lista[mid]

    def moda(self):
        conteo = Counter(self.lista)
        maxf = max(conteo.values())
        modas = [x for x, f in conteo.items() if f == maxf]

        if len(modas) == len(conteo):
            return None  # Sin moda real
        return modas

    def suma(self):
        return sum(self.lista)

    def suma_cuadrados(self):
        return sum(x*x for x in self.lista)

    def minimo(self):
        return self.lista[0]

    def maximo(self):
        return self.lista[-1]

    def rango(self):
        return self.maximo() - self.minimo()

    def varianza(self, muestra=False):
        μ = self.media()
        if muestra:
            return sum((x - μ)**2 for x in self.lista) / (self.n - 1)
        return sum((x - μ)**2 for x in self.lista) / self.n

    def desviacion_estandar(self, muestra=False):
        return math.sqrt(self.varianza(muestra))
    def resumen(self):
        return {
            "n": self.n,
            "media": self.media(),
            "promedio": self.promedio(),
            "mediana": self.mediana(),
            "moda": self.moda(),
            "mínimo": self.minimo(),
            "máximo": self.maximo(),
            "rango": self.rango(),
            "suma": self.suma(),
            "suma de cuadrados": self.suma_cuadrados(),
            "varianza poblacional": self.varianza(),
            "varianza muestral": self.varianza(muestra=True),
            "desv. estándar poblacional": self.desviacion_estandar(),
            "desv. estándar muestral": self.desviacion_estandar(muestra=True)
        }
