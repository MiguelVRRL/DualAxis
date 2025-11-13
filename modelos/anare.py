import numpy as np
import scipy.stats as stats


class Anare:
    def __init__(self, n:int,b1:float,nivel_confianza: float, x: list[int | float], y: list[int | float ]) -> None:
        self.__n: int = n
        self.__b1 = b1
        self.__nivel_confianza = nivel_confianza
        self.__arr_x = np.array(x)
        self.__arr_y = np.array(y)
        self.__arr_Y_potencia = np.array([yi**2 for yi in y])
        self.__arr_xy = np.array([x[i]*y[i] for i in range(len(x))])


    def glr(self) -> int:
        return 1

    def gle(self) -> int:
        return self.__n-2
    def glt(self) -> int:
        return self.gle() + self.glr()
    def sce(self) -> float:
        return self.sct()-self.scr()
    def sct(self) -> float: 
        return float(self.__arr_Y_potencia.sum() - (self.__arr_y.sum()/self.__n)) 
    def scr(self) -> float:
        return float(self.__b1 * (self.__arr_xy.sum() - (self.__arr_x.sum()*self.__arr_y.sum()/self.__n)))
    def cmr(self) -> float:
        return self.scr()/self.glr()
    def cme(self) -> float:
        return self.sce()/self.gle()
    def fc(self) -> float:
        return self.cmr()/self.cme()



