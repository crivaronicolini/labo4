from marco import experimento
import numpy as np
import matplotlib.pyplot as plt
termo = experimento("termometria/diados")
# termo.mediciones(claves=["medi",'csv'])
archivos = [
        # ['medicion_calentar_1amp_2.csv',18.0],
        # ['medicion_apagar_1amp_2.csv',18.0],
        # ['medicion_calentar_1amp_3.csv',18.0],
        # ['medicion_calentar_1amp_4.csv',18.0],
        # ['medicion_enfriar_1-5amp_1.csv',18.0],
        # ['medicion_apagado_1-5amp_1.csv',18.0],
        # ['medicion_calentar_2amp_1.csv',18.0],
        # ['medicion_calentar_1-75amp_1.csv',18.0],
        ['medicion_enfriar_1-75amp_1.csv',18.0],
        # ['medicion_enfriar_1-75amp_prueba.csv',18.0],
        ]
def plotear(labels,*args):
    # labels = ['Termo1','Termo2','Voltaje']
    for i,var in enumerate(args):
        plt.plot(S,var,'.',label=labels[i])

    plt.title(medicion.split('.')[0])
    plt.legend(loc='best')
    plt.ylabel('Temperatura (C)')
    plt.xlabel('Tiempo (S)')
    # plt.show()
    # plt.savefig(medicion.split('.')[0])

def pasarT(A):
    tablatermo = np.loadtxt("termometria/diados/tablatermo3.csv", dtype='float', delimiter=',')
    # tablatermo = tablatermo.ravel()
    Anormal = np.interp(A,tablatermo[:,1],tablatermo[:,0])
    # Acambiado = np.interp(-A,tablatermo[:,1],tablatermo[:,0])
    return Anormal

for medicion,tamb in archivos:
    try:
        T1,T2,S = termo.cargar(medicion,3)
        # T1_ = pasarT(T1)
        # T2_ = pasarT(T2)
        # plotear(['T1','T2'],T1_,T2_)
        T1 = pasarT(T1)
        T2 = pasarT(T2)
        T1, T2 = -T1,-T2
        plotear(['T1cambiado','T2cambiado'],T1,T2)
        # print(T1cam,T2cam,S)
        temps = np.hstack((T1,T2,S))
        ar = medicion.replace('enfriar','calentar').replace('medicion','tempnuevas')
        np.savetxt(ar, temps,fmt='%.6f', delimiter=',')
    # print(temps[:,0])
    # print(T1)
    # plotear(['T1', 'Temps'],T1,temps[:,0])
    # plt.show()
    # break
    # T1 = pasarT(T1)
    # T2 = pasarT(T2)
    # plt.clf()
    except ValueError:
        continue
    #     T1,T2,V,S = termo.cargar(medicion,4)
    #     plotear(T1,T2,V)

    plt.show()
