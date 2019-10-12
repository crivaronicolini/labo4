from marco import experimento
# import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt

termo = experimento('.')
termo.mediciones(claves=['barrido'])
print(termo.archivos)

res = ['_barrido_0-1_resonancia_2_',
        'barrido_0-1Hz_resonancia',
        'barrido_0-5Hz_resonancia',
        'barrido_0-5Hz_resonancia (2)',
        'barrido_1Hz_resonancia']
pico = ['7_barrido_2-5Hz_pico150',
        '8_barrido_1Hz_pico150_2',]
antires = ['barrido_1Hz_antiresonancia',
        'barrido_1Hz_antiresonancia2',]

todos = [res, pico, antires]

# def plotear(X, *args):
#     labels = ['Frecuencia','Voltaje Cuarzo','Voltaje']
#     for i,var in enumerate(args):
#         plt.plot(X,var,'.',label=labels[i])

#     # plt.title(medicion.split('.')[0])
#     # plt.legend(loc='best')
#     plt.xlabel('Frecuencia')
#     plt.ylabel('Voltaje Cuarzo')
#     # plt.show()
#     # plt.savefig(medicion.split('.')[0])

# plt.ion()
def main():
    for lista in [res,pico]:
        for medicion in lista:
            # print(f'ploteando {medicion}')

            data = pd.read_csv(medicion, names=['f', 'A1', 'A2', 'Tr'],
                    delim_whitespace=True, header=0)
            data.plot.scatter(data)
            # data.plot.scatter(x='f', y='Tr')
            # f,A1,A2,Tr = termo.cargar(medicion,4)
            # plotear(f,A2)
            # plt.show()
    print('finish')
    # plt.show()

# plt.ioff()
# plt.show()
main()
