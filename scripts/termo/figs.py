'''
TODO
    hacer grafico dv vs dt ajustar y sacar alpha
        graficar por separado calentar y enfriar
    plotear delta temps contra los volts para las resistencias
    comparar graficos del mismo proceso(enfriando con y sin voltage, etc)
    estimar efecto joule

'''
from marco import experimento
import warnings
import numpy as np
import matplotlib.pyplot as plt
from uncertainties import unumpy as un

plt.rcParams['mathtext.default']= 'regular'
termo = experimento("termometria/diados/tempsposta")
# termo.mediciones(claves=["temp",'csv'])
archivos = [
        ['tempnuevas_apagar_1amp_2.csv',18.0,0,0
        ],['tempnuevas_enfriar_1amp_2.csv',18.0,0.97,0.7
        ],['tempnuevas_apagado_1-5amp_1.csv',18.0,0,0
        ],['tempnuevas_enfriar_1amp_3.csv',18.0,1,0.7
        ],['tempnuevas_enfriar_1amp_4.csv',18.0,1,0.7
        ],['tempnuevas_enfriar_1-5amp_1.csv',18.0,1.5,1.1

        ],['tempnuevas_enfriar_2amp_1.csv',18.0,1.98,1.4
        # ],['tempnuevas_enfriar_2amp_1.csv',18.0,1.98,1.4

        ],['tempnuevas_calentar_1-75amp_1.csv',18.0,1.74,1.3
        # ],['tempnuevas_enfriar_1-75amp_prueba.csv',18.0

        ],['temperaturas_recalentar_1-75_1.csv',18.0,1.74,1.7
        ],['temperaturas_enfriar_1-75amp_2.csv',18.0,1.74,1.2
        ],['temperaturas_recalentar_2amp_1.csv',18.0,2.01,1.5
        ],['temperaturas_enfriar_1-25amp_1.csv',18.0,1.25,0.9

        # ],['temperaturas_res_1amp_1.csv',18.5,0,0
        # ],['temperaturas_res_enfriando_03amp_1.csv',18.5,0,0
        # ],['temperaturas_res_05amp_1.csv',18.5,0.49,4.7
        # ],['temperaturas_res_enfriando_05amp_1.csv',19.0,0,0

        ]]


# print(len(termo.mediciones))
# print(len(archivos))
def plotear(X,Y,sig,label):
    try:
        varvals = un.nominal_values(Y).ravel()
        varerr = un.std_devs(Y).ravel()
        print('caca')
        print(varerr)
        X = X.ravel()
        Xerr = 0.1 * np.ones(np.shape(X))
        varmenos = varvals - varerr
        varmas = varvals + varerr
        print(medicion)
        plt.errorbar(X,varvals,xerr=Xerr,yerr=varerr,fmt=sig,label=label)

        # plt.plot(X,varvals,'ok')
        # plt.fill_between(X,varmenos.ravel(),varmas.ravel(), alpha=0.5)
    except TypeError:
        print('no andan lo errores')
        plt.plot(S,var,'.')

    # plt.title(medicion.split('.')[0].replace('_',' '))
    # plt.legend(loc='best')
    # plt.ylabel('Temperatura (C)')
    # plt.xlabel('Tiempo (S)')
    # plt.show()
    # plt.savefig(medicion.split('.')[0])

def errorT(A,err,tamb):
    e = err * np.ones(np.shape(A))
    Ar = un.uarray(A,e)
    Ar = Ar + un.uarray(tamb,0.5)
    return Ar

def errorV(A,err):
    e = err * np.ones(np.shape(A))
    Ar = un.uarray(A,e)
    return Ar

def rendimiento(A1,A2):
    #veo de las temperaturas cual minimo es el menor y saco el dT
    #correspondiente
    minimo = min(np.min(A1),np.min(A2))
    base = T1[T1==minimo]
    if base.size > 0:
        resultado = T2[T1==minimo] - base
        # print(medicion,resultado)
    else:
        warnings.warn('estan dados vuelta')
        base = T2[T2==minimo]
        resultado = T1[T2==minimo] - base
        # print(medicion,resultado)
    return resultado

def rendimiento2(A1,A2):
    #uso los ultimos valores de cada medicion pq son mas estables.
    #vale para todas las mediciones salvo las que tienen prendido y apagado
    resultado = A1[-1] - A2[-1]
    if resultado < 0:
        resultado = A2[-1] - A1[-1]
    return resultado


deltas = []
amps = []
# volts = []
for medicion,tamb,amp,volt in archivos:
    try:
        labels = ['Termo1','Termo2']
        T1,T2,S = termo.cargar(medicion,3)
        T1 = errorT(T1,2.2,tamb)
        T2 = errorT(T2,2.2,tamb)
        # print(medicion)
        if medicion == 'tempnuevas_enfriar_1amp_3.csv':
            delta = rendimiento(T1,T2)
        else:
            delta = rendimiento2(T1,T2)
        deltas.append(delta)
        amps.append(amp)
        # volts.append(volt)
	# plotear(labels,T1,T2)
	# plotear('Delta T',T1-T2)
    except ValueError:
        continue
        labels = ['Termo1','Termo2','Voltaje']
        T1,T2,V,S = termo.cargar(medicion,4)
        T1 = errorT(T1,2.2,tamb)
        T2 = errorT(T2,2.2,tamb)
        V = errorV(V,1)
        # plotear(labels,T1,T2)
        # plotear(['Delta T', 'Voltaje',T1-T2,V)
# deltas = np.asarray(deltas)
# labels = ['delta T','Amperaje']

deltaTmax = max(deltas)
deltaTnorm = deltas / deltaTmax
amps = np.asarray(amps)
mask = deltaTnorm > 0.6
mask = mask.ravel()
plotear(amps[mask], deltaTnorm[mask],'xk', 'Calentar')
plotear(amps[~mask], deltaTnorm[~mask],'ok','Enfriar')
# for i in range(len(deltas)):
#     plt.plot(amps,un.nominal_values(deltas),'.')
#     xy=(volts[i],un.nominal_values(deltas)[i])
#     plt.annotate(archivos[i][0],xy=xy)
    # xy_=(volts[i],un.nominal_values(deltas)[i])
    # plt.annotate(archivos[i][0],xy=xy,xytext=xy_,textcoords='offset points')

# deltas =  un.nominal_values(deltas).ravel()deltas + 273
# volts = volts * 1000
# print(un.nominal_values(deltas))
# z = np.polyfit(volts, un.nominal_values(deltas).ravel(),1)
# polinomio = np.poly1d(z)
# print(z)
# pendiente = x[0]
# x = np.linspace(min(volts),max(volts),100)
# plt.plot(x,polinomio(x),'r',label=f'alpha ={z[0]}')
plt.grid(True)
plt.ylabel(r'$\Delta T / \Delta T_{max}$')
plt.xlabel(r'$Corriente\ (A)$')
plt.legend(loc='upper left', framealpha=1)
plt.savefig('rendimiento.png', dpi=300)
# plt.show()
