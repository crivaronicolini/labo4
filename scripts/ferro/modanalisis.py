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
import sys
from scipy.signal import savgol_filter

try:
    archivo = sys.argv[1]
    # plt.ion()
except IndexError:
    print("script")
    archivo = '29-August-2019_00-48-28_T-9x49.csv'
#Divido el csv por columnas: Primario, Secundario, Temp, Voltaje de T
P, S, T, V = np.loadtxt(archivo, delimiter=',', unpack=True,
        max_rows=1000)
# P, S, T, V = np.hsplit(data[:1000,:],4)

#Centro la figura
P = P - np.mean(P)
S = S - np.mean(S)
Pf=1
# Pf = savgol_filter(P.reshape(-1), 51 ,2)
# Sf = savgol_filter(S.reshape(-1), 51 ,2)

def test(C,D,A=P,B=S):
    f, (hys, cur) = plt.subplots(1,2)
    hys.plot(A,B)
    hys.plot(C,D)
    curvas = [A,B,C,D]
    labels = str(i for i in curvas)
    hys.grid(True)
    f.tight_layout()
    for i in curvas:
        cur.plot(np.arange(len(i)),i)
        cur.legend(labels)
    f.show()
    # cur.plot(A,B)
    # cur.plot(C,D)



#separo los elementos de la cola con masked arrays
# p = P.ravel()
# s = S.ravel()

div = np.divide((P.max()-P.min()),6)
a = P[P>(P.max() - div)]
b = S[P>(P.max() - div)]
# cola = np.array(a,b)
# plt.ion()
x = np.polyfit(a,b,1)
# polinomio = np.poly1d(x)
pendiente = x[1]
angulo = np.arctan(pendiente)
plt.plot(x)
plt.plot(P,S)

#crea matriz de rot y aplica a datos
c, s = np.cos(angulo), np.sin(angulo)
R = np.array(((c,-s), (s, c)))
matRot = R @ np.vstack((P,S))
Pr = matRot[0,:]
Sr = matRot[1,:]
# Pr, Sr = np.hsplit(np.dot(np.hstack((P,S)),R),2)

plt.grid(True)
test(Pr, Sr)

# if Pf:
#     test(Pr, Sr)
# if not Pf:
#     plt.figure(1)
#     plt.plot(P,S)
#     plt.plot(Pr,Sr)
#     plt.figure(2)
#     plt.plot(Pr)
#     plt.plot(Sr)
#     plt.grid(True)
#     plt.show()
# else:
#     return


# plt.plot(a,b)

plt.show()
