# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 20:51:35 2019
Ajustes
proceso:
    cargo datos
    selecciono columnas
    selecciono pico y t max de los datos
    cuentas
    defino funcion transferencia
    ajusto, le doy los parametros que aproxime
    
@author: ingri
"""
import numpy as np
#from numpy  import exp, sin, sqrt, pi
from lmfit import Model
import matplotlib.pyplot as plt
from uncertainties import ufloat

# Cargo los datos
datos = np.loadtxt(r'C:\Users\ingri\OneDrive\Documentos\Labo 4\Piezo\intento2\ajuste\medidas2.txt')

#selecciono columnas
w_1 = datos[:,0]
t_1 = datos[:,1]
error = datos[:,2]

#Pico
pico = t_1 == np.max(t_1) #le pregunta cuando t_1 es maximo
decay = np.max(t_1)/np.sqrt(2) #decae por sqrt(2)
mask = np.abs(t_1 - decay) < 0.00205 #busca los dos valores mas cercanos, acomodar el epsilon
anchos = w_1[mask]
dw = anchos[1] - anchos[0]

#def find_nearest(t_1, decay): #busca el valor mas cercano a decay en mis datos
#    minimo = (np.abs(t_1 - decay)).argmin()
#    return t_1[minimo]

#Cuentas
w0 = w_1[pico][0] #frecuencia de resonancia
y0 = t_1[pico][0] #transferencia en resonancia
R2 = 9860.0 #res que medimos con el multimetro

Q = (w0/dw)
R = R2/y0 - R2
L = (Q*(R + R2))/w0
C = 1/((w0*w0)*L)

#    defino la funcion transferencia
def transfer(x, R, C, L):
    return R2/(np.sqrt((R+R2)**2 + (x*L - 1/(x*C))**2))

# esto era para chequear que sea parecido el modelo a los datos antes de fittear
#w = np.linspace(50075,50110)
#y = transfer(w, R, R2, L, C)
#
#plt.plot(w,y)
#plt.plot(w_1,t_1)
#plt.show
#------------
    
# Ajuste

gmodel = Model(transfer)
result = gmodel.fit(t_1, x=w_1, R=R, L=L, C=C)
print(result.fit_report())

#plt.scatter(w_1,t_1, marker = 'o', c = 'k', s= 5)
#plt.errorbar(w_1, t_1,yerr=error, fmt = ' ', c = 'dimgray', alpha=0.5)
##plt.plot(w_1, result.init_fit, 'k--', label='initial fit')
#plt.plot(w_1, result.best_fit, 'r-', label='best fit')
#plt.legend(loc='best')
##plt.show()

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

# Para configurar el grid (start, stop, step)
x_major_ticks = np.arange(50070, 50115, 5)
x_minor_ticks = np.arange(50070, 50115, 2.5)
y_major_ticks = np.arange(0, 0.6, 0.1)
y_minor_ticks = np.arange(0, 0.5, 0.05)

x_major_ticks[5] = 50096.

ax.set_xticks(x_major_ticks)
ax.set_xticks(x_minor_ticks, minor=True)
ax.set_yticks(y_major_ticks)
ax.set_yticks(y_minor_ticks, minor=True)

ax.grid(which='both')
#----------------------------

#ax.plot(w_2,t_2, c='k')
ax.scatter(w_1,t_1, marker = 'o', c = 'k', s= 5)
ax.errorbar(w_1, t_1,yerr=error, fmt = ' ', c = 'dimgray', alpha=0.5)
ax.plot(w_1, result.best_fit, 'r-')
ax.set_xlabel('Frecuencia (Hz)')
ax.set_ylabel('Transferencia')
ax.set_xlim(50070,50115)

ax.axvline(50096, c='r')

#vuelvo a buscar pico y ancho pero para el fit
pico = result.best_fit == np.max(result.best_fit)
t_res = result.best_fit[pico][0]
decay2 =  np.max(result.best_fit)/np.sqrt(2) #decae por sqrt(2)
mask = np.abs(result.best_fit - decay) < 0.00205 #busca los dos valores mas cercanos, acomodar el epsilon
anchos = w_1[mask]
dw = anchos[-1] - anchos[0]
w0 = w_1[pico][0]
Q = w0/dw
wa = ufloat(50283.9, 0.2)
C2 = 1/((wa*wa*L) - (1/C))
print('w0 =', w0, 'Q= ', Q, 'ancho= ', dw)
#plt.savefig('res_osci_1.png',dpi=300)
#plt.show()