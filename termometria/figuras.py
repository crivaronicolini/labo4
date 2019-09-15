import os
import matplotlib.pyplot as plt
import numpy as np
#os.chdir("~/Documents/fac/labo4/termometria/")
archivos = [i for i in os.listdir() if i.startswith("temperaturas")==True and i.endswith("csv")==True]
otros = ['temperaturashieloamb2.csv','temperaturashielocaliente1.csv','temperaturashieloamb3.csv']
nova = ['temperaturashieloamb1.csv','temperaturas1.csv','temperaturashieloamb4.csv']
# archivos = [i for i in archivos if i not in nova]
archivos = ['temperaturashielocaliente1.csv','temperaturashielocaliente2.csv', 'temperaturashieloamb2.csv', 'temperaturashieloamb3.csv', 'temperaturascalientehielo1.csv']
ex = ['hielo a caliente 1', 'hielo a caliente 2','hielo a ambiente 2', 'hielo a ambiente 3', 'caliente a hielo 1']
datos = [np.loadtxt(i,delimiter=',') for i in archivos]
fig = plt.figure(figsize=(8.27,11.69),dpi=300)
axes = fig.subplots(5,1)
# print(axes)
plt.ion()
for i, (archivo,dato,ax) in enumerate(zip(archivos,datos,axes)):
    P,T,L,S = np.hsplit(dato,4)
    serror = 0.1*np.ones(len(S))
    terror = 2.2*np.ones(len(T))
    perror = 2*np.ones(len(P))
    lerror = 2.2*np.ones(len(L))
    # if archivo in nova:
    #     continue
    if archivo in otros:
        ax.errorbar(range(len(P)),P,yerr=perror,xerr=serror,fmt='none',color='k',label=None)
        ax.errorbar(range(len(T)),T,yerr=terror,xerr=serror,fmt='none',color='k',label=None)
        ax.errorbar(range(len(L)),L,yerr=lerror,xerr=serror,fmt='none',color='k',label=None)
        Pplot = ax.plot(range(len(P)),P,'-',color='k')
        Tplot = ax.plot(range(len(T)),T,'-.',color='k')
        Lplot = ax.plot(range(len(L)),L,':',color='k')
        # pass
    else:
        ax.errorbar(S,P,yerr=perror,xerr=serror,fmt='none',color='k',label=None)
        ax.errorbar(S,T,yerr=terror,xerr=serror,fmt='none',color='k',label=None)
        ax.errorbar(S,L,yerr=lerror,xerr=serror,fmt='none',color='k',label=None)
        Pplot = ax.plot(S,P,'-',color='k')
        Tplot = ax.plot(S,T,'-.',color='k')
        Lplot = ax.plot(S,L,':',color='k')
    ax.set_title(ex[i])
    #plt.savefig(archivo.split('.')[0] +".png")

# handles, labels = axes[0].get_legend_handles_labels()
# handles = [h[0] for h in handles]

plt.xlabel('Tiempo (S)')
left, width = -.07, .5
bottom, height = .25, .5
right = left + width
top = bottom + height
plt.text(left, 0.5*5.*(bottom+top), 'Temperatura (C)',
        horizontalalignment='right',
        verticalalignment='center',
        rotation='vertical',
        transform=ax.transAxes)
# plt.ylabel('Temperatura (C)')
fig.subplots_adjust(left=0.1, wspace=0.1, hspace=0.28, bottom=0.05,top=0.95)
fig.legend(['PT100','Termocupla','LM35'],loc='upper left')
# fig.tight_layout()
# fig.show()
fig.savefig("todos.png")
# fig.savefig("todos.png",  bbox_inches='tight')
