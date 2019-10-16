# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 15:38:39 2019
 Frec; X; Y; R; Theta
@author: ingri
"""

from uncertainties import ufloat
from uncertainties import unumpy
import numpy as np
import os
import matplotlib.pyplot as plt

##################### CARGO LOS DATOS
#path = r'C:\Users\ingri\OneDrive\Documentos\Labo 4\Piezo\antiresonancia\barrido'
#archivos = os.listdir(path)
#os.chdir(r'C:\Users\ingri\OneDrive\Documentos\Labo 4\Piezo\antiresonancia')
## importe datos, seleccione columnas, hice cuentas, propague y guarde
#total=np.zeros((1,5))
#for archivo in archivos :
#    nombre = r'C:\Users\ingri\OneDrive\Documentos\Labo 4\Piezo\antiresonancia\barrido\\' + archivo
#    dir = np.loadtxt(nombre, delimiter = ';', skiprows = 1)
##    print(archivo)
#    vout = dir[:,3]
#    w_1 = dir[:,0]
#    fase = dir[:,4]
#    vin = ufloat(0.380, 0.380*0.03)  #poner aca el Vpp de entrada
#    evout = unumpy.uarray(vout, vout*0.01)
#    ffase = unumpy.uarray(fase, 0.008)
#    vfase = unumpy.nominal_values(ffase)
#    efase = unumpy.std_devs(ffase)
#    tran = evout/vin
#    vtran = unumpy.nominal_values(tran)
#    etran = unumpy.std_devs(tran)
#    data1 = np.column_stack((w_1, vtran, etran, vfase, efase))
##    data2 = np.concatenate(data1, axis=0)
#    total = np.vstack((total,data1))
##    print(total)
#
#np.savetxt('antitodosjuntos.txt', total)
#########################

datos = np.loadtxt(r'C:\Users\ingri\OneDrive\Documentos\Labo 4\Piezo\antiresonancia\antitodosjuntos.txt', skiprows = 1)
#selecciono columnas
w_1 = datos[:,0]
t_1 = datos[:,1]
et_1 = datos[:,2]
fase = datos[:,3]
efase = datos[:,4]

#grafico de prueba
#plt.scatter(w_1,t_1)
#plt.scatter(w_1,fase)
#plt.show()

########## VER UNA POR UNA CUALES SON LAS MEDIDAS QUE SE DEFORMAN
#test = np.loadtxt(r'C:\Users\ingri\OneDrive\Documentos\Labo 4\Piezo\antiresonancia\barrido\Busco_antires_50282_50286_9e-0212-38-03_.txt', skiprows=1, delimiter= ';')
#
#vout = test[:,3]
#vin = 0.380
#t_1 = vout/vin
#w_1 = test[:,0]
#fase = test[:,4]
#
#mask = t_1 > 0.0015
#plt.scatter(w_1,t_1)
#plt.show()
###########

########### ANALISIS

pico = t_1 == np.min(t_1)
w01 = w_1[pico][4]
y0 = t_1[pico][0]
ew01 = 0.2

#findfrec = np.where(w_1 == 50283.)
#w_2 = w_1[152:170]
#t_2 = t_1[152:170]
#fase2 = fase[152:170]
#
#plt.scatter(w_2,fase2)
#z = np.polyfit(w_2,fase2,1)
#p = np.poly1d(z)
#w0fase = np.roots(p)

#grafico definitivo
fig = plt.figure()
ax1 = fig.add_subplot(2, 1, 1) #agrega el primer plot
ax2 = fig.add_subplot(2, 1, 2) #agrega el segundo plot

############################# plot del zoom
#                         (start, stop, step)
#x_major_ticks = np.arange(50282., 50286., 1)
##x_minor_ticks = np.arange(50282, 50286, 1)
#
#y1_major_ticks = np.arange(0, 0.006, 0.0001)
##y1_minor_ticks = np.arange(0, 0.5, 0.0001)
#
#y2_major_ticks = np.arange(-100, 100, 25)
#y2_minor_ticks = np.arange(-100,100, 25)
#
#x_major_ticks[2] = 50283.9

############################## plot sin zoom
#                        (start, stop, step)
x_major_ticks = np.arange(50255., 50315., 5)
#x_minor_ticks = np.arange(50282, 50286, 1)

y1_major_ticks = np.arange(0, 0.002, 0.005)
#y1_minor_ticks = np.arange(0, 0.5, 0.0001)

y2_major_ticks = np.arange(-100, 100, 25)
y2_minor_ticks = np.arange(-100,100, 25)

x_major_ticks[2] = 50284.

ax1.set_xticks(x_major_ticks)
#ax1.set_xticks(x_minor_ticks, minor=True)
ax1.set_yticks(y1_major_ticks)
#ax1.set_yticks(y1_minor_ticks, minor=True)

ax2.set_xticks(x_major_ticks)
#ax2.set_xticks(x_minor_ticks, minor=True)
ax2.set_yticks(y2_major_ticks)
ax2.set_yticks(y2_minor_ticks, minor=True)

ax1.grid(which='both')
ax2.grid(which='both')
#----------------------------

#ax.plot(w_2,t_2, c='k')
ax1.scatter(w_1,t_1, marker = 'o', c = 'tab:blue', s= 5)
ax1.errorbar(w_1, t_1,yerr=et_1, fmt = ' ', c = 'dimgray', alpha=0.5)
ax2.scatter(w_1,fase, marker = 'o', c = 'tab:orange', s=5)
ax2.errorbar(w_1,fase, yerr = efase, fmt = ' ', c='dimgray', alpha=0.5)
ax1.set_xlabel('Frecuencia (Hz)')
ax1.set_ylabel('Transferencia')

############## zoom
#ax1.set_xlim(50282,50286)
#ax1.set_ylim(-0.00001,0.0005)
#ax2.set_xlim(50282,50286)
#ax2.set_ylim(-60,75)

############# sin zoom
ax1.set_xlim(50255,50315)
ax1.set_ylim(-0.00001,0.002)
ax2.set_xlim(50255,50315)
ax2.set_ylim(-100,100)


ax2.set_xlabel('Frecuencia (Hz)')
ax2.set_ylabel('Fase')
#para marcar donde esta la resonancia
ax1.axvline(50283.9, c='r')
ax2.axvline(50283.9, c='r')
plt.tight_layout()
ax1.ticklabel_format(axis='x', useOffset=False)
ax2.ticklabel_format(axis='x', useOffset=False)

