import pandas as pd
from matplotlib.figure import Figure


class GraficoBarra:
    def __init__(self, data_frame: pd.DataFrame, titulo: str) -> None:
        self.__data_frame = data_frame
        lista = self.__data_frame[titulo].to_list()
        lista.sort(reverse=True)
        self.__fig = Figure(figsize=(5, lista[0]), dpi=100)
        self.__axes = self.__fig.add_subplot(111)
        self.__data_frame.plot(kind="bar",ax=self.__axes,title=titulo, use_index=True, legend=False)


    def get_grafico(self):
        return self.__fig

    def guardar_grafico(self,nombre_archivo: str):
        if nombre_archivo:
            self.__fig.savefig(nombre_archivo)
