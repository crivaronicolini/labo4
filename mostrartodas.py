from marco import experimento
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
termo = experimento("termometria/diados/tempsposta")
termo.mediciones(claves=["temp",'csv'])
print(termo.mediciones)

def plotear(*args):
    labels = ['Termo1','Termo2','Voltaje']
    for i,var in enumerate(args):
        plt.plot(S,var,'.',label=labels[i])

    plt.title(medicion.split('.')[0])
    # plt.legend(loc='best')
    plt.ylabel('Temperatura (C)')
    plt.xlabel('Tiempo (S)')
    # plt.show()
    # plt.savefig(medicion.split('.')[0])

for medicion in tqdm(termo.mediciones):
    try:
        T1,T2,S = termo.cargar(medicion,3)
        if medicion == 'tempnuevas_calentar_1-75amp_1.csv':
            plotear(T1,T2)
        else:
            plotear(T1+18,T2+18)
        plt.savefig(termo.absdire+ '/figuras/' + medicion + '.png',dpi=300)
        # plt.show()
        plt.clf()
    except ValueError:
        continue
        T1,T2,V,S = termo.cargar(medicion,4)
        plotear(T1,T2,V)
