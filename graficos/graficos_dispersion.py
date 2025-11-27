from matplotlib.figure import Figure
import pandas as pd


class GraficoDispersion:
    def __init__(self, atributo_x, atributo_y,titulo_x,titulo_y) -> None:
        self.__data_frame = pd.DataFrame({titulo_x:atributo_x,titulo_y:atributo_y})
        self.__fig = Figure(figsize=(5, 4), dpi=100)
        self.__axes = self.__fig.add_subplot(111)
        self.__data_frame.plot.scatter(x=titulo_x,y=titulo_y,  ax=self.__axes)

    def get_grafico(self):
        return self.__fig

    def guardar_grafico(self,nombre_archivo: str):
        if nombre_archivo:
            self.__fig.savefig(nombre_archivo)
