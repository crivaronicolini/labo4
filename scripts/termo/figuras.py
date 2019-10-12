import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from lmfit import Model

fig, ax = plt.subplots(1,1)
colores = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red']

plt.ion()
mediciones = [1]
# mediciones = range(4)

def ajuste(T,Tc,a,B):
    return np.multiply(a,np.power((Tc-T),B))

for i in mediciones:
    T, m = np.hsplit(np.load(f"datosmt{i+1}.npy"),2)
    # print('T es :')
    # print(T)
    # # terror = etermocupla + edigit + etemp amb
    # # terror = 2.2C + temp(1/(2^16)) + 1C
    #V(edigit)
    # # merror = adq(digitalizacion de S y promedio en picos)
    # # merror = (10/(2^16)) + 
    #m es la suma entre dos V(sdaq) y el promedio entre 7 picos de esa suma
    # # ax.plot(T,m,'.',c=colores[i])

# ax.set_xlim(-125,0)
# ax.xaxis.set(ticks=np.arange(-120,1,10))

# plt.xlabel("Temperatura (C)")
# plt.ylabel("Magnetización")
# plt.show()


    #ajusto beta
    # ln(T - Tc) = b ln(m)
    # T = T - 273
    #Tc = -3

    ##AJUSTE
    #lt = np.log(Tc - T).ravel()
    #lm = np.log(m/np.max(m)).ravel()
    #beta = np.divide(lm,lt)
    #mascara=(lm<-1.0) & (lm>-3)
    #z = np.polyfit(lt[mascara],lm[mascara],1)
    #print(z)
    #pol = np.poly1d(z)
    #ax.plot(-lt,lm, '.',c=colores[i])
    #ax.plot(-lt, beta, '.',c='k')
    #ax.plot(-lt[mascara], pol(lt[mascara]),c=colores[i], label=f"medicion{i+1},beta={z[0]}")

    #grafico del paper
    # M = np.power(m/np.max(m),(1/0.3645))
    # ax.plot(T, M,'.',c=colores[i],label="beta=0.3645")

    # mascara=(M<.7) & (M>.07)
    # z = np.polyfit(T[mascara],M[mascara],1)
    # print(z)
    # pol = np.poly1d(z)
    # ax.plot(T[mascara], pol(T[mascara]),c=colores[i], label=f"medicion{i+1},beta={z[0]}")
    # M = np.power(m/np.max(m),(1/0.5))
    # ax.plot(T, M,'.',c='k', label=f"medicion{i+1}, beta=0.5")


    #Ajuste con funcion
    # def ajuste(T,Tc,a,B):
    #     return a*(Tc-T)**(B)
    # print(ajuste(-6,-3,0.3,1))
    # T = T + 273
    # popt, pcov = curve_fit(ajuste, T.ravel(), m.ravel())
    # popt, pcov = curve_fit(ajuste, T.ravel(), m.ravel(), bounds=([-8.,0,0.3],[0,1.,0.6]))
    # plt.plot(T.ravel()+273, ajuste(T.ravel(), *popt), 'r-', label='fit: Tc=%5.3f, a=%5.3f, B=%5.3f' % tuple(popt))
    # plt.plot(T, ajuste(T.ravel(),(-6),0.1,0.3645, 0.3),'--', c='k')
    # plt.plot(T+273, m,'.',c=colores[i])

    #ajusto con lmtib
    print('ajustando')
    print(len(T))
    amt = 13
    T = T + 273.15
    terror = np.ones(np.shape(T))* np.sqrt((2.2)**2 +(1/(2^16))**2 +1)
    merror = np.ones(np.shape(T))* 0.0003
    plt.errorbar(T, m,fmt='.',xerr=terror, yerr=merror)

    T = T[:amt]
    m = m[:amt]

    gmodel = Model(ajuste)
    result = gmodel.fit(m, T=T, Tc=-5+273.15, a=1, B=0.3, nan_policy='propagate')

    print(result.fit_report())

    # plt.plot(T, result.init_fit, 'k--', label='initial fit')
    plt.plot(T, result.best_fit, 'r-', label='Ajuste')

plt.ioff()

# plt.xlabel("ln(Tc-T)")
# plt.ylabel("ln(Ms)")
plt.legend(loc='upper right')
plt.grid(True)
plt.xlabel("Temperatura (K)")
plt.ylabel("Mr",fontsize=12)
# ax.set_xlim(170,280)
plt.savefig("curvamvsTAJUSTEmedicion2Kelvin.png",dpi=300)
plt.show()
