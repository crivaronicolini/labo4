'''
TODO
    +hacer grafico dv vs dt ajustar y sacar alpha
        -graficar por separado calentar y enfriar
    -plotear delta temps contra los volts para las resistencias
    -comparar graficos del mismo proceso(enfriando con y sin voltage, etc)
    -estimar efecto joule

'''
from marco import experimento
import warnings
import numpy as np
import matplotlib.pyplot as plt
from uncertainties import unumpy as un

plt.rcParams['mathtext.default']= 'regular'
termo = experimento("cacatermometria/diados/tempsposta")
# termo.mediciones(claves=["temp",'csv'])
archivos = [
        ['tempnuevas_apagar_1amp_2.csv',18.0,0,0
        ],['tempnuevas_enfriar_1amp_2.csv',18.0,0.97,0.7
        ],['tempnuevas_apagado_1-5amp_1.csv',18.0,0,0
        ],['tempnuevas_enfriar_1amp_3.csv',18.0,1,0.7
        ],['tempnuevas_enfriar_1amp_4.csv',18.0,1,0.7
        ],['tempnuevas_enfriar_1-5amp_1.csv',18.0,1.5,1.1

        ],['tempnuevas_enfriar_2amp_1.csv',18.0,1.98,1.4

        ],['tempnuevas_calentar_1-75amp_1.csv',18.0,1.74,1.3
        # ],['tempnuevas_enfriar_1-75amp_prueba.csv',18.0

        ],['temperaturas_recalentar_1-75_1.csv',18.0,1.74,1.7
        ],['temperaturas_enfriar_1-75amp_2.csv',18.0,1.74,1.2
        ],['temperaturas_recalentar_2amp_1.csv',18.0,2.01,1.5
        ],['temperaturas_enfriar_1-25amp_1.csv',18.0,1.25,0.9

        ],['temperaturas_res_1amp_1.csv',18.5,0,0
        ],['temperaturas_res_enfriando_03amp_1.csv',18.5,0,0
        ],['temperaturas_res_05amp_1.csv',18.5,0.49,4.7
        ],['temperaturas_res_enfriando_05amp_1.csv',19.0,0,0

        ]]


# print(len(termo.mediciones))
# print(len(archivos))
def plotearS(style,*args):
    for i,var in enumerate(args):
        try:
            varerr = un.std_devs(var)
            varvals = un.nominal_values(var)

            varmenos = varvals - varerr
            varmas = varvals + varerr

            # plt.errorbar(S,varvals,yerr=varerr,fmt='.',label=labels[i])
            plt.plot(S.ravel(),varvals,'.',color=style[i])
            plt.fill_between(S.ravel(),varmenos.ravel(),varmas.ravel(), color=style[i], alpha=0.3)
        except TypeError:
            print('no andan lo errores')
            plt.plot(S,var,'.',label=labels[i])

    # plt.title(medicion.split('.')[0].replace('_',' '))
    # plt.legend(loc='best')
    plt.ylabel('Temperatura (C)')
    plt.xlabel('Tiempo (s)')
    # plt.show()
    # plt.savefig(medicion.split('.')[0])
def plotear2(X,V):
    try:
        varvals = un.nominal_values(V)
        varerr = un.std_devs(V)

        varmenos = varvals - varerr
        varmas = varvals + varerr

        xerr = un.std_devs(X) / 2
        x = un.nominal_values(X)

        # plt.errorbar(x,varvals,xerr=xerr,yerr=varerr,fmt='o')
        plt.plot(x,varvals,'ok')
        plt.fill_between(x,varmenos,varmas,color='k', alpha=0.3)
        plt.fill_betweenx(varvals, x-xerr,x+xerr,color='k',alpha=0.3)
    except TypeError:
        print('no andan lo errores')
        plt.plot(S,var,'.')

    # plt.title(medicion.split('.')[0].replace('_',' '))
    # plt.legend(loc='best')
    plt.ylabel(r'$Voltaje\ (V)$')
    plt.xlabel(r'$\Delta T\ estacionario\ (K)$')

def errorT(A,err,tamb):
    e = err * np.ones(np.shape(A))
    Ar = un.uarray(A,e)
    Ar = Ar + un.uarray(tamb,0.5)
    return Ar

def errorV(A):
    e = 0.0030 * A + 0.0030*100*np.ones(np.shape(A))
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

def fiteo(x,y):
    x = un.nominal_values(x)
    yerr = un.std_devs(y)
    y = un.nominal_values(y)
    # x = x + 273
    # y = y*1000
    z,cov = np.polyfit(x,y,1,w=yerr,cov=True)
    zerr = np.sqrt(cov[0,0] * np.sqrt(len(y)))
    polinomio = np.poly1d(z)
    h = np.linspace(min(x),max(x),100)
    # plt.plot(h,polinomio(h),'--w',label=fr'$\alpha =({1e3*z[0]:.1f} \pm {1e3*zerr:.1f}) \ mV \ K^{-1}$')
    #en volts da (0.053 +- 0,001)V
    plt.plot(h,polinomio(h),'--w',label=r'$\alpha =(59.9 \pm 0.4) \  mV \ K^{-1}$')


for medicion,tamb,amp,volt in archivos:
    try:
        styles = ['k','grey']
        T1,T2,S = termo.cargar(medicion,3)
        T1 = errorT(T1,2.2,tamb)
        T2 = errorT(T2,2.2,tamb)
        # print(medicion)
        plotearS(styles,T1,T2)
        # plotear('Delta T',T1-T2)
        # plt.legend(loc='upper left', framealpha=1)
        plt.grid(True)
        # plt.savefig('./termometria/diados/tempsposta/figuras/' + medicion.split('.')[0]+ '.png', dpi=300)
        plt.show()
        plt.clf()


    except ValueError:
        continue
        labels = ['Termo1','Termo2','Voltaje']
        T1,T2,V,S = termo.cargar(medicion,4)
        T1,T2,V,S = T1.ravel(), T2.ravel(), V.ravel(), S.ravel()
        T1 = errorT(T1,2.2,tamb)
        T2 = errorT(T2,2.2,tamb)
        V = errorV(V)
        V = 1e-2 * V
        # print(un.std_devs(V))
        # plotearS(labels,T1,T2,d)
        # print(V)
        plt.legend(loc='upper left', framealpha=1)
        plt.grid(True)
        plt.show()
        # plotearS(labels,T1,T2,V)
        # print(V)
# deltas = np.asarray(deltas)
# labels = ['delta T','Amperaje']

# deltaTmax = max(deltas)
# deltaTnorm = deltas / deltaTmax

# deltas = np.asarray(deltas) + 273
# volts = np.asarray(volts)
# # for i in range(len(deltas)):
#     # plt.plot(un.nominal_values(deltas),volts,'.')
#     # xy=(un.nominal_values(deltas)[i],volts[i])
#     # plt.annotate(archivos[i][0],xy=xy)
#     # xy_=(volts[i],un.nominal_values(deltas)[i])
#     # plt.annotate(archivos[i][0],xy=xy,xytext=xy_,textcoords='offset points')

# dT = un.nominal_values(deltas).ravel()
# dTerr = un.std_devs(deltas).ravel()



# x = np.linspace(min(dT),max(dT),100)
# plt.plot(x,polinomio(x),'--k',label=r'$\alpha =(629.0 \pm 44.6) \ \mu V \ K^{-1}$')
# # plt.plot(x,polinomio(x),'--k',label=fr'$\alpha =({z[0]:.1f} \pm {zerr:.1f}) \ \mu V\ K^{-1}$')


# plt.ylabel(r'$Voltaje\ (V)$')
# plt.xlabel(r'$\Delta T\ estacionario\ (K)$')
# plt.legend(loc='upper left')
# # plt.show()
# plt.savefig('alfaenfriar.png', dpi=300)
