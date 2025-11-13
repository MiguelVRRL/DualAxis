import math
import numpy as np

class RegresionLineal:
    def __init__(self,nivel_confianza: float, x: list[int | float], y: list[int | float]) -> None:
        self.__arr_x = np.array(x)
        self.__arr_y = np.array(y)
        self.__arr_x_potencia = np.array(map(lambda x: x**2, x))
        self.__arr_y_potencia = np.array(map(lambda y: y**2, y))
        self.__arr_xy = np.array([y[i]*x[i] for i in range(len(x))])
        self.__x_prom: float = self.__arr_x.sum()/self.__arr_x.size
        self.__y_prom: float = self.__arr_y.sum()/self.__arr_y.size
        
        self.n: int = len(x)
        self.nivel_confianza: float = nivel_confianza
        self.var_x: float = self.varianza_x()
        self.var_y: float = self.varianza_y()
        self.var_cov_xy: float = self.cov_xy()
        self.var_r: float = self.r()
        self.var_b1: float = self.b1()
        self.var_b0: float = self.b0()
     



    def varianza_x(self) -> float:
        return math.sqrt((float(self.__arr_x_potencia.sum())/self.n)-(self.__x_prom**2))
    
    def varianza_y(self) -> float:
        return math.sqrt((float(self.__arr_y_potencia.sum())/self.n)-(self.__y_prom**2))
    def r(self) -> float:
        return (self.var_cov_xy/(self.var_x*self.var_y))
   
    def cov_xy(self) -> float:
        return (float(self.__arr_xy.sum())/self.n)-(self.__y_prom*self.__x_prom)

    def b1(self) -> float:
        return self.var_r*(self.var_y/self.var_x)

    def b0(self) -> float:
        return self.__y_prom - (self.var_b1*self.__x_prom)
    
    def coeficiente_determinacion(self) -> float:
        return self.var_r**2 
    
    def y_estimado(self, x: float | int) -> float | int:
        return self.var_b0+(self.var_b1*x)
    
    def evaluacion_R(self) -> str:
        if self.var_r >= 0.5:
            return "Hay relacion"
        elif self.var_r < 0.5 or self.var_r > 0.2:
            return "Probablemente no hay relacion"
        else:
            return "No hay relacion"

    
