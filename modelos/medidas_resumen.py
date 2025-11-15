import numpy as np

class MedidasResumen:
    def __init__(self,x: list[int | float ], fr: list[int] = []) -> None:
        self.__x: list[int | float ] = x
        self.__n: int = len(x)
        self.__fr = fr

    def sumatoria(self) -> int | float:
        return sum(self.__x) 
    def promedio(self)-> int  | float:
        return self.sumatoria()/self.__n

    def sumatoria_cuadrado(self)-> int | float:
        return sum(map(lambda x: x**2,self.__x))

    def analisis_aux(self)->float:
        x_prom: int | float = self.promedio() 
        return sum(map(lambda x: x - x_prom,self.__x))

    def varianza_poblacional_cuadrado(self)->float:
        return self.analisis_aux()/self.__n

    def varianza_poblacional(self)->float:
        return sqrt(self.varianzapoblacional_cuadrado())

    def varianzamuestral_cuadrado(self)->float:
        return self.analisis_aux()/(self.__n-1)

    def varianza_muestral(self)->float:
        return sqrt(self.varianzamuestral_cuadrado())
