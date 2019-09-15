'''
quiero hacer una clase que tenga metodos utiles para mediciones
metodos
   pasarle un directorio y que me devuelva archivos
       archivos = med.dir("directorio")
   pasarle un archivo y que devuelva array
       array = med.arr(archivo)
       que ese array sea de instancias de la clase variables
   asociarle errores
       necesito que cada variable de una medicion exista por si misma
       X.error(error)
   grficarlo

experimento
   medicion
       variables, array
'''
import matplotlib.pyplot as plt
import numpy as np
import os
class experimento():
    "una clase para agilizar la carga de datos"
    def __init__(self, dire):
        self.dire = dire
        self.absdire = os.path.abspath(dire) + '/'

    def mediciones(self, claves=[]):
        self.mediciones = sorted(os.listdir(self.dire))
        if claves!=[]:
            self.mediciones = [i for i in self.mediciones if all(clave in
                i for clave in claves)]
        else: pass
        return self.mediciones

    def cargar(self,medicion, columnas):
        arch = self.absdire + medicion
        print(arch)
        self.csv = np.loadtxt(arch, delimiter=',')
        variables = np.hsplit(self.csv,columnas)
        return variables


exp = experimento("termometria")
mediciones = exp.mediciones(claves=['temperaturas', 'csv'])
otros = ['temperaturashieloamb2.csv','temperaturashieloamb3.csv']

for medicion in mediciones:
    P,T,L,S = exp.cargar(medicion,4)
    if medicion in otros:
        plt.plot(P)
        plt.plot(T)
        plt.plot(L)
    else:
        plt.plot(S,P)
        plt.plot(S,T)
        plt.plot(S,L)
    plt.show()

