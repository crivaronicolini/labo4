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
import sys, os
from scipy.signal import savgol_filter
import pdb

dir = "/home/marco/Documents/fac/labo4/ferro/mediciones/medicion3/"
archivos = sorted(os.listdir(dir))

# try:
#     archivo = sys.argv[1]
#     # plt.ion()
# except IndexError:
#     print("script")
#     archivo = '29-August-2019_00-48-28_T-9x49.csv'
# plt.grid(True)
# plt.plot(P,S)
# Pf=1
# Pf = savgol_filter(P.reshape(-1), 51 ,2)
# Sf = savgol_filter(S.reshape(-1), 51 ,2)

# def test(C,D,A=P,B=S):
#     f, (hys, cur) = plt.subplots(1,2)
#     hys.plot(A,B)
#     hys.plot(C,D)
#     curvas = [A,B,C,D]
#     labels = str(i for i in curvas)
#     hys.grid(True)
#     f.tight_layout()
#     for i in curvas:
#         cur.plot(np.arange(len(i)),i)
#         cur.legend(labels)
#     f.show()
    # cur.plot(A,B)
    # cur.plot(C,D)


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
    #si cruza el eje
    mascara = (A>-0.02) & (A<0.02)
    print(np.count_nonzero(mascara))

    cerosP = A[mascara]
    magnetizacion = B[mascara]
    return np.mean(np.absolute(magnetizacion))


def tMedia(T):
    return np.mean(T.T), np.std(T.T)


def load(archivo):
    data = np.loadtxt(dir + '/' + archivo, delimiter=',')

    #Divido el csv por columnas: Primario, Secundario, Temp, Voltaje de T
    return np.hsplit(data[:1000,:],4)

#def getT(V):
#    #funcion para pasar del voltaje a la temp real de termocupla
#    P, S, _, V = load(archivo[1])
#    C = np.array[]
#    T = np.power(V,[0,1,2,3,4])
def getT(archivo):
    P, S, U, V = load(archivo)
    # C = np.array([0.0,0.394501280250e-01,0.236223735980e-04,-0.328589067840e-06])
    C = np.array([0.0000000E+00,
         2.5173462E+01,
        -1.1662878E+01,
        -1.0833638E+01,
        -8.9773540E-02,
        -3.7342377E-02,
        -8.6632643E-03,
        -1.0450598E-03,
        -5.1920577E-04])

    T = C * np.power(V * 1000,range(9))
    T = np.sum(T,axis=1)
    # plt.plot(V * 1000, 'r')
    # pdb.set_trace()
    plt.plot(U, 'r')
    plt.plot(T, 'b')
    plt.show()

getT(archivos[0])



def main(archivos):
    archivos = (i for i in archivos if i.endswith('.csv'))
    for archivo in archivos:

        P, S, T, V = load(archivo)

        #Centro la figura
        P = P - np.mean(P)
        S = S - np.mean(S)

        Pr, Sr = autorotar(P,S)
        m = mag(P,S)
        mRot = mag(Pr,Sr)

        t = np.mean(T)
        resultado = [t, m, mRot]
        # plt.ion()
        print(f"{archivo[18:]} tiene resultado {resultado}")
        plt.plot(t, m, '.', c='b')
        plt.plot(t, mRot, '.', c='r')


    plt.xlabel('Temperatura (C)')
    plt.ylabel('Magnetizacion')
    plt.show()





# plt.grid(True)
# test(Pr, Sr)

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

# plt.show()
