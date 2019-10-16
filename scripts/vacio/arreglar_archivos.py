import pandas as pd
import numpy as np
from marco import experimento
import matplotlib.pyplot as plt
'''tengo que empalmar las distintas mediciones que estan en un mismo archivo'''
vacio = experimento('/home/marco/Documents/fac/labo4/vacio/', claves=['.txt'])

for a in vacio:
    m = vacio.cargar_pd(a)
    sep = m[m['Tiempo'] == 'Tiempo']
    loc = list(sep.T) #esto agarra las posiciones donde estan los separadores
    loc.append(len(m))
    #loc=[925,1868]

    for i,v in enumerate(loc[:-1]):
        ultimo_t = float(m['Tiempo'].iloc[loc[i] -1 ])
        c = loc[i+1] - loc[i] -1
        d = m['Tiempo'].iloc[loc[i]+1:loc[i+1]] = m['Tiempo'].iloc[loc[i]+1:loc[i+1]].astype('float') + ultimo_t*np.ones((c,))
        print(d)
        print(ultimo_t)
        # if loc[:-1] == v:
        #     pass
    loc[-1] -= 1
    m = m.drop(loc)
    m = m.astype('float64')
    m = m.drop(columns='$Medicion')
    m.to_csv(a)
