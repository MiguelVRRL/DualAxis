import pandas as pd
import math




class TablaDatos:
    def __init__(self, ubicacion: str = "") -> None:
        self.set_nuevos_datos(ubicacion)
    def set_dataFrame(self, dataFrame: pd.DataFrame) -> None:
        self.__data_frame = dataFrame
    def set_nuevos_datos(self, ubicacion: str = "") -> None:
        if ubicacion == "":
            self.__ubicacion = ""
            self.__ext = ""
            self.__data_frame = pd.DataFrame()
            return
        self.__ubicacion: str = ubicacion
        aux: list[str] = ubicacion.split(".")
        self.__ext: str = aux[len(aux)-1]
        match aux[len(aux)-1]:
            case "csv":
                self.__data_frame: pd.DataFrame = pd.read_csv(ubicacion)
            case "xlsx" | "xlsm" | "xls" | "xlsb":
                self.__data_frame: pd.DataFrame = pd.read_excel(ubicacion)
            case "txt":
                self.__data_frame: pd.DataFrame = pd.read_csv(ubicacion,delimiter="\t")
            case _:
                return
    def get_tipo(self,columna: str) -> str:
        if self.__data_frame[columna].dropna().apply(lambda x: isinstance(x, str)).all():
            return "literal"
        elif pd.api.types.is_bool_dtype(self.__data_frame[columna]):
            return "bool"
        elif pd.api.types.is_float_dtype(self.__data_frame[columna]):
            return "continuo"
        elif pd.api.types.is_integer_dtype(self.__data_frame[columna]):
            return "discreto"
        return "discreto"
    def get_atributos(self, *tipo_excluido):
        if not tipo_excluido:
            return self.__data_frame.columns.to_list()
        lista_aux = self.__data_frame.columns.to_list()
        for i in lista_aux.copy():
            tipo_actual = self.get_tipo(i)

            if tipo_actual in tipo_excluido:
                lista_aux.remove(i)
        return lista_aux
    def get_num_atributos(self) -> int:
        return self.__data_frame.shape[1]
    def get_num_elems_total(self) -> int:
        return self.__data_frame.size
    def get_ocurrencias(self, columna: str):
        match self.get_tipo(columna):
            case "literal":
                return pd.DataFrame({columna:self.__data_frame[columna].value_counts().to_dict()})

            case "bool":
                return self.__data_frame.value_counts().to_frame()
            case "continuo":
                lista_datos = self.__data_frame[columna].value_counts().to_dict()
                lista_llaves = list(lista_datos.keys())
                lista_llaves.sort()
                lista_valores = list(lista_datos.values())
                mayor_valor = lista_llaves[len(lista_llaves)-1]
                menor_valor = lista_llaves[0]
                rango = mayor_valor-menor_valor
                num_clases = int(1 + 3.22*math.log10(sum(lista_valores)))
                c = rango/num_clases
                diccionario_rangos = {}
                aux = ""
                for i in range(num_clases):
                    aux = f"{menor_valor+(i*c)}-{menor_valor+((i+1)*c)}"
                    diccionario_rangos[aux] = 0
                    for j in range(len(lista_llaves)):
                        # print("menor valor: ",menor_valor+(i*c), " comparacion: ",lista_llaves[j], " resultado: ", menor_valor+(i*c) >= lista_llaves[j])
                        # print("mayor valor: ",menor_valor+((i+1)*c)," comparacion: ", lista_llaves[j], " resultado: ",lista_llaves[j] < menor_valor+((i+1)*c))

                        if (menor_valor+(i*c) < lista_llaves[j]) and (lista_llaves[j] < menor_valor+((i+1)*c)) :
                            diccionario_rangos[aux] += lista_datos[lista_llaves[j]]
                return pd.DataFrame({columna:diccionario_rangos})
            case "discreto":
                lista_datos = self.__data_frame[columna].value_counts().to_dict()
                lista_llaves = list(lista_datos.keys())
                lista_llaves.sort()
                lista_valores = list(lista_datos.values())
                mayor_valor = lista_llaves[len(lista_llaves)-1]
                menor_valor = lista_llaves[0]
                rango = mayor_valor-menor_valor
                num_clases = int(1 + 3.22*math.log10(sum(lista_valores)))
                c = rango//num_clases
                diccionario_rangos = {}
                aux = ""
                for i in range(num_clases):
                    aux = f"{menor_valor+(i*c)}-{menor_valor+((i+1)*c)}"
                    diccionario_rangos[aux] = 0
                    for j in range(len(lista_llaves)):
                        # print("menor valor: ",menor_valor+(i*c), " comparacion: ",lista_llaves[j], " resultado: ", menor_valor+(i*c) >= lista_llaves[j])
                        # print("mayor valor: ",menor_valor+((i+1)*c)," comparacion: ", lista_llaves[j], " resultado: ",lista_llaves[j] < menor_valor+((i+1)*c))

                        if (menor_valor+(i*c) <= lista_llaves[j]) and ( lista_llaves[j] <  menor_valor+((i+1)*c) or (i==num_clases-1 and lista_llaves[j] <=  menor_valor+((i+1)*c)) )  :
                            diccionario_rangos[aux] += lista_datos[lista_llaves[j]]
                return pd.DataFrame({columna:diccionario_rangos})
    def get_valores(self, columna: str):
        return self.__data_frame[columna]

    def get_num_elems_grupo(self, columna_x: str, columna_y: str) -> int:
        return self.__data_frame.groupby([columna_x,columna_y])[columna_x].count().loc[columna_x]
    def get_num_elems(self, columna: str) -> int:
        return self.__data_frame[columna].size

    def get_dataFrame(self):
        return self.__data_frame
    def get_ubicacion(self) -> str:
        return self.__ubicacion
    def guardar_archivo(self,ubicacion: str = "") -> None:
        if ubicacion != "":
            self.__ubicacion = ubicacion
            aux: list[str] = ubicacion.split(".")
            self.__ext: str = aux[len(aux)-1]
        if self.__ubicacion == "":
            return
        match self.__ext:
            case "csv":
                self.__data_frame.to_csv(self.__ubicacion,index=False)
            case "xlsx" | "xlsm" | "xls" | "xlsb":
                self.__data_frame.to_excel(self.__ubicacion,index=False)
            case "txt":
                self.__data_frame.to_csv(self.__ubicacion,sep="\t",index=False)
            case _:
                return
    
