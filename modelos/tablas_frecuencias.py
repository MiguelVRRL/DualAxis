import pandas as pd

class TablaFrecuencia:
    def __init__(self, x: pd.DataFrame,titulo: str, tipo: str ) -> None:
        self.__titulo = titulo
        self.__tipo: str = tipo
        self.__x = x 
        self.__n = sum(self.__x.to_dict('list')[self.__titulo])
    def valores(self):
        return list(self.__x.to_dict()[self.__titulo].keys())
    def fi(self):
        return self.__x.to_dict('list')[self.__titulo]
    def mc(self):
        return list(map(lambda x: (float(x.split("-")[0]) + float(x.split("-")[1]))/2 ,self.valores()))
    def fr(self):
        return list(map(lambda x: x/self.__n,self.fi()))
    def frp(self):
        return list(map(lambda x: x*100,self.fr()))
    def fia(self):
        fi = self.fi()
        acc = fi[0]
        fia  = [acc]
        for i in range(1,len(fi)):
            acc += fi[i]
            fia.append(acc)
        return fia
    def fra(self):
        return list(map(lambda x: x/self.__n,self.fia()))

    def frap(self):
        return list(map(lambda x: x*100,self.fra()))
    def fiaa(self):
        fi = self.fi()
        acc = self.__n
        fia  = [acc]
        for i in range(1,len(fi)):
            acc -= fi[i]
            fia.append(acc)
        return fia
    def fraa(self):
        return list(map(lambda x: x/self.__n,self.fiaa()))

    def frapa(self):
        return list(map(lambda x: x*100,self.fraa()))

    def get_tabla(self):
    
    
        tabla = [self.valores(),self.fi(),self.fr(),self.frp(),self.fia(),self.fra(),self.frap()]   
        if self.__tipo in [ 'continuo' , 'discreto'] :
                tabla.insert(2,self.mc())
                tabla.append(self.fiaa())
                tabla.append(self.fraa())
                tabla.append(self.frapa())

        return self.transponer_matriz(tabla)
    def get_headers(self):
        if self.__tipo in ["continuo",'discreto']:
            return ["Intervalos",'fi','mc','fr','fr%','fia','fra','fra%','fia*','fra*','fra%*']
        return ["Intervalos",'fi','fr','fr%','fia','fra','fra%']


    def transponer_matriz(self,matriz):
        if not matriz or not matriz[0]:
            return []
    
        filas = len(matriz)
        columnas = len(matriz[0])
    
        # Crear matriz transpuesta
        transpuesta = [[matriz[j][i] for j in range(filas)] for i in range(columnas)]
    
        return transpuesta

