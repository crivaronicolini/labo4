'''
autor: marco
py 3.7

Diagrama del analisis:
    Sacar offset restando el promedio
    Filtrar la señal para sacar ruido
    Calcular Ms
'''


import numpy as np
import matplotlib.pyplot as plt
from matplotlib import transforms
import sys
from scipy.signal import savgol_filter

try:
    archivo = sys.argv[1]
except IndexError:
    archivo = '29-August-2019_00-48-28_T-9x49.csv'
data = np.loadtxt(archivo, delimiter=',')
#Divido el csv por columnas: Primario, Secundario, Temp, Voltaje de T
P, S, T, V = np.hsplit(data[:1000,:],4)

#Centro la figura
P = P - np.mean(P)
S = S - np.mean(S)
Pf=0
# Pf = savgol_filter(P.reshape(-1), 51 ,2)
# Sf = savgol_filter(S.reshape(-1), 51 ,2)

def test(C,D,A=P,B=S):
    f, (hys, cur) = plt.subplots(1,2)
    hys.plot(A,B)
    hys.plot(C,D)
    curvas = [A,B,C,D]
    labels = str(i for i in curvas)
    f.tight_layout()
    for i in curvas:
        cur.plot(np.arange(len(i)),i)
        cur.legend(labels)
    f.show()
    # cur.plot(A,B)
    # cur.plot(C,D)

#crea matriz de rot y aplica a datos
tita = np.radians(5)
c, s = np.cos(tita), np.sin(tita)
R = np.array(((c,-s), (s, c)))

Pr, Sr = np.hsplit(np.dot(np.hstack((P,S)),R),2)

# plt.ion()
if Pf:
    test(Pf, Sf)
if not Pf:
    plt.plot(P,S)
    plt.plot(Pr,Sr)
    plt.grid(True)
    plt.show()
