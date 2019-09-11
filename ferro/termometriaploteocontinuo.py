'''
TODO
hacer que plotee en tiempo real
agregar configuraciones
'''
from __future__ import division, unicode_literals, print_function, absolute_import

import visa
import numpy as np
import matplotlib.pyplot as plt
import time

print('hola ingro')

# Este string determina el intrumento que van a usar.
# Lo tienen que cambiar de acuerdo a lo que tengan conectado.
#le pongo nombre a los instrumentos
lm35 = 'GPIB0::22::INSTR'
pt100 = 'GPIB0::23::INSTR'
termocupla = 'GPIB0::24::INSTR'
rm = visa.ResourceManager()
#me dice los nombres de los instrumentos
#rm.list_resources()

lm35 = rm.open_resource(lm35)
pt100 = rm.open_resource(pt100)
termocupla = rm.open_resource(termocupla)

devices = [pt100, termocupla, lm35]
for i in devices:
    print(i.query('CONF?')
#configuraciones
# SYSTem:BEEPer





tablatermo = np.loadtxt("tablatermo.csv", dtype='float', delimiter=',')
tablapt100 = np.loadtxt("tablapt100.csv", dtype='float', delimiter=',')
tablatermo = tablatermo.ravel()
tablapt100 = tablapt100.ravel()

plt.ion()
temps=[]
datos = []

duracion = 60
inicio = time.time()
despues = inicio + duracion

while time.time() < despues:
    print("hola")

    vlm35 = float(lm35.query('MEASURE:VOLTAGE:DC? MIN,MIN'))
    vtermo = 1000 * float(termocupla.query('MEASURE:VOLTAGE:DC? MIN,MIN'))
    rpt100 = float(pt100.query('MEASURE:FRES? 1000,MIN'))
    pt100.write('SYST:BEEP')

    tiempo = time.time() - inicio
    lista = [rpt100,vtermo,vlm35,tiempo]
    datos.append(lista)

    tpt100 = np.interp(rpt100,tablapt100[:,1],tablapt100[:,0])
    ttermo = np.interp(vtermo,tablatermo[:,1],tablatermo[:,0])
    tlm35 = vlm35 *100
    temps.append([tpt100,ttermo,tlm35, tiempo)
    plt.plot(tiempo, rpt100, tiempo, ttermo, tiempo, tlm35)

    # time.sleep(0.5)

np.set_printoptions(precision=5, suppress=True)
nummedicion='hielocaliente2'
np.savetxt(f"medicion{nummedicion}.csv", datos, fmt='%.6f', delimiter=',')

#para pasar a t
# for i in range(len(datos)):
#     tpt100 = np.interp(datos[i][0],tablapt100[:,1].ravel(),tablapt100[:,0].ravel())
#     ttermo = np.interp(datos[i][1],tablatermo[:,1].ravel(),tablatermo[:,0].ravel())
#     tlm35 = datos[i][2] *100
#     temps.append([tpt100,ttermo,tlm35, datos[i][3]])


atemps =np.asarray(temps)
print(atemps)
# np.savetxt(f"temperaturas{nummedicion}.csv", atemps, fmt='%.6f', delimiter=',')
#temps = np.array([tpt100, ttermo, vlm35, float(mercurio)])
#print(temps)





