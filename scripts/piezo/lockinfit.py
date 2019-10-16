# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 11:48:43 2019

@author: ingri
"""

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

# Cargo los datos
datos = np.loadtxt(r'C:\Users\ingri\OneDrive\Documentos\Labo 4\Piezo\todosjuntos.txt', skiprows = 1)

#selecciono columnas
w_1 = datos[:,0]
t_1 = datos[:,1]
error = datos[:,2]
fase = datos[:,3]
efase = datos[:,4]

#Pico #NO TOCAR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
pico = t_1 == np.max(t_1) #le pregunta cuando t_1 es maximo
decay = np.max(t_1)/np.sqrt(2) #decae por sqrt(2)
epsilon = 0.005
mask = np.abs(t_1 - decay) < epsilon #busca los dos valores mas cercanos, acomodar el epsilon
anchos = w_1[mask]
dw = anchos[-1] - anchos[0]

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
    
#################### Ajuste
gmodel = Model(transfer)
result = gmodel.fit(t_1, x=w_1, R=R, L=L, C=C)
print(result.fit_report())
#t_2 = t_1 + 0.05

################### Grafico
fig = plt.figure()
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)

# Para configurar el grid (start, stop, step)
x_major_ticks = np.arange(50070, 50115, 5)
x_minor_ticks = np.arange(50070, 50115, 2.5)
y_major_ticks = np.arange(0, 0.6, 0.1)
y_minor_ticks = np.arange(0, 0.5, 0.05)

y2_major_ticks = np.arange(-100,100,20)
#y2_minor_ticks = np.arange(-90,90,10)

x_major_ticks[5] = 50096.

ax1.set_xticks(x_major_ticks)
ax1.set_xticks(x_minor_ticks, minor=True)
ax1.set_yticks(y_major_ticks)
ax1.set_yticks(y_minor_ticks, minor=True)

ax2.set_xticks(x_major_ticks)
ax2.set_xticks(x_minor_ticks, minor=True)
ax2.set_yticks(y2_major_ticks)
#ax2.set_yticks(y2_minor_ticks, minor=True)

ax1.grid(which='both')
ax2.grid(which='both')
#----------------------------

#ax.plot(w_2,t_2, c='k')
ax1.scatter(w_1,t_1, marker = 'o', c = 'k', s= 5)
ax1.errorbar(w_1, t_1,yerr=error, fmt = ' ', c = 'dimgray', alpha=0.5)
ax1.plot(w_1, result.best_fit, 'r-', label = 'ajuste')
ax1.set_xlabel('Frecuencia (Hz)')
ax1.set_ylabel('Transferencia')
ax1.set_xlim(50075,50115)

ax2.scatter(w_1,fase, marker = 'o', c = 'k', s= 5)
ax2.errorbar(w_1, fase,yerr=efase, fmt = ' ', c = 'dimgray', alpha=0.5)
ax2.set_xlabel('Frecuencia (Hz)')
ax2.set_ylabel('Fase')
ax2.set_xlim(50075,50115)

ax1.axvline(50096., c='r')
ax2.axvline(50096., c='r')
#vuelvo a buscar pico y ancho pero para el fit
pico = result.best_fit == np.max(result.best_fit)
t_res = result.best_fit[pico][0]
decay2 =  np.max(result.best_fit)/np.sqrt(2) #decae por sqrt(2)
epsilon = 0.01
mask = np.abs(result.best_fit - decay) < epsilon #busca los dos valores mas cercanos, acomodar el epsilon
anchos = w_1[mask]
dw = anchos[-1] - anchos[0]
w0 = w_1[pico][0]
Q = w0/dw
plt.show()
print('w0 =', w0, 'Q= ', Q, 'ancho= ', dw)

#findfrec = np.where(w_1 == 50096.)
#w_2 = w_1[60:70]
#t_2 = t_1[60:70]
#fase2 = fase[60:70]
#
#plt.scatter(w_2,fase2)
#z = np.polyfit(w_2,fase2,1)
#p = np.poly1d(z)
#w0fase = np.roots(p)
##plt.show()