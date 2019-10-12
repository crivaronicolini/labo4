'''
autor: marco
py 3.7

Diagrama del analisis:
    Sacar offset restando el promedio
    Filtrar la señal para sacar ruido
    Calcular Ms en funcion de temp
    Rotar los graficos para que queden bonitos
    ???
    Profit
'''


import numpy as np
import matplotlib.pyplot as plt
import sys, os, pdb
from scipy.signal import savgol_filter


def test(C,D,A,B):
    #funcion para probar filtros y como quedan las señales
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
    cur.plot(A,B)
    cur.plot(C,D)


def autorotar(P,S):
    #separo los elementos de la cola con masked arrays
    p = P.ravel()
    s = S.ravel()
    #la cola esta formada por, digamos, el sexto superior e 
    #inferior de cada onda
    div = (p.max()-p.min()) / 6
    a = p[p>(p.max() - div)]
    b = s[p>(p.max() - div)]
    #ajusto solo la pendiente
    x = np.polyfit(a,b,1)
    polinomio = np.poly1d(x)
    pendiente = x[0]
    angulo = np.arctan(pendiente) - 0.01

    #crea matriz de rot y aplica a datos
    cos, sen = np.cos(angulo), np.sin(angulo)
    R = np.array(((cos,-sen), (sen, cos)))
    Pr, Sr = np.hsplit(np.dot(np.hstack((P,S)),R),2)
    return Pr,Sr

def mag(A,B):
    #saco magnetizacion, P = 0 no ocurre porque son muestras discretas,
    #pero si cruza el eje
    mascara = (A>-0.02) & (A<0.02)
    magnetizacion = B[mascara]
    return np.mean(np.absolute(magnetizacion))

def load(archivo):
    data = np.loadtxt(dir + '/' + archivo, delimiter=',')
    #Divido el csv por columnas: Primario, Secundario, Temp, Voltaje de T
    return np.hsplit(data[:3000,:],4)

def getT(V):
    C = np.array([0.0000000E+00,
         2.5173462E+01,
        -1.1662878E+01,
        -1.0833638E+01,
        -8.9773540E-02,
        -3.7342377E-02,
        -8.6632643E-03,
        -1.0450598E-03,
        -5.1920577E-04])

    T = C * np.power(V,range(9))
    T = np.sum(T,axis=1)
    return np.mean(-1 * T)

def temp(A):
    tabla = np.array([[-220,-6.158],
                     [-210,-6.035],
                     [-200,-5.891],
                     [-190,-5.730],
                     [-180,-5.550],
                     [-170,-5.354],
                     [-160,-5.141],
                     [-150,-4.913],
                     [-140,-4.669],
                     [-130,-4.411],
                     [-120,-4.138],
                     [-110,-3.852],
                     [-100,-3.554],
                     [-90,-3.243],
                     [-80,-2.920],
                     [-70,-2.587],
                     [-60,-2.243],
                     [-50,-1.889],
                     [-40,-1.527],
                     [-30,-1.156],
                     [-20,-0.778],
                     [-10,-0.392],
                     [0., 0.000]])
    T = np.interp(A * 1,tabla[:,1],tabla[:,0])
    return np.mean(T)

def main(archivos, color, medicion):
    archivos = (i for i in archivos if i.endswith('.csv'))

    for archivo in archivos:
        P, S, U, V = load(archivo)
        T = temp(V)
        # T_ = getT(V)
        if medicion == "medicion3":
            T = T * 10
        T = T + 22.
        U = np.mean(U)

        #Centro la figura
        P = P - np.mean(P)
        S = S - np.mean(S)

        # Pr, Sr = autorotar(P,S)
        m = mag(P,S)
        # mRot = mag(Pr,Sr)

        np.set_printoptions(formatter={'float': '{: 0.3f}'.format})
        resultado = np.array([np.mean(V), T, U,  m])
        print(f"{archivo[18:]} tiene resultado {resultado}")

        # plt.plot(T, m, '.', c=(0.1, 0.1, color[i]))
        plt.plot(T, m, '.', c=color)
        # plt.plot(U, m, '.', c='b')

    plt.xlabel('Temperatura (C)')
    plt.ylabel('Magnetizacion')

for i in range(4):
    dir = "/home/marco/Documents/fac/labo4/ferro/mediciones/medicion" + str(i+1)
    archivos = sorted(os.listdir(dir))
    print(f"mediciones de medicion{i+1}")
    colores = ['r','g','b','k']
    color = colores[i]
    plt.ion()
    main(archivos, color, "medicion" + str(i+1))
plt.ioff()
plt.show()
