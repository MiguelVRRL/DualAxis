import numpy as np
import math
class TablaFrecuencia:
    def __init__(self, x: list[int | float]) -> None:
        self.__x: list[int | float ] = x.sort()
        self.__arr_x = np.array(self.__x)
        self.__n: int = sum(x)
        self.__k: int = int(1+3.32*math.log10(self.__n))
        self.__rango: int | float = self.__x[self.__n-1]-self.__x[0]
        self.__n_decimales = 0
        if type(self.__x[0]) == float:
            self.__n_decimales = len(str(self.__x[0]).split(".")[len(self.__x[0].split["."])-1])
        
            # aux = str(self.__x[0]) # [12.2,122,5] -> "12.2"
            # list = aux.split(".") # 12.2 -> ["12","2"]
            # ultimo elemento= aux[len(aux)-1] # ["12","2"] -> "2"
            # n_decilames = len(ultimo elemento)  # "2" -> 1
        self.__c: int | float = round(self.__rango/self.__k, self.__n_decimales)
        self.__r_ideal: int | float = self.__c*self.__k

    def frecuencia_absoluta(self) ->int:
       return self.__n

    def frecuencia_relativa(self) -> list[int]:
        return map(lambda x: x/self.__n,self.__x)

    def frecuencia_rela_porcentual(self) ->float:
        return map(lambda  x: x*100,self.frecuencia_relativa())+"%"
    
    def f_acumulada_ascendente(self)->int:
        lista_aux: list[int] = [self.__x[0]]
        for i in range(1,len(self.__x)-1,1):
            lista_aux[i] = self.__x[i] + self.__x[i-1]
        return lista_aux
    
    def f_relativa_porcentual(self)->float:
        return map(lambda x: x*100,self.f_acumulada_ascendente())+"%"
    
    def f_acumulada_descendente(self)->int:
        list_aux: list[int]= [self.f_acumulada_ascendente[self.__x]]
        for i in range(0,len(self.__x)-1,1):
            list_aux[i+1] = list_aux[i] - self.__x[i]
        return list_aux
    
    def f_rel_acumulada_descendente(self)->float:
        return map(lambda  x: x/self.__n,self.f_acumulada_descendente())
    
    def f_rel_acumulada_descendente_porcentual(self)->float:
        return map(lambda x: x*100 ,self.f_rel_acumulada_descendente())