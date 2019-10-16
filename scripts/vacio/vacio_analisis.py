from marco import experimento
import numpy as np
from lmfit import Model
import matplotlib.pyplot as plt
import pandas as pd
# from uncertainties import unumpy as un



Po = 37.56 #I*V de lamparita
# T = Temperatura #C
# t = tiempo #s

def make_params():
    espesor = 0.472 #m
    Area = (((3.82/2000)**2)*np.pi) #m**2
    C_esp = 0 #J*C/g
    epsilon = 1. #emisividad casi 1
    sigma = 1.38e-23 #cte boltz JC
    Tamb = 0
    h = 0 #param caracteristico

    gamma = Area(4*sigma*epsilon*(Tamb)**3 + h) #m**2 J C**4
    tau = (espesor*C_esp*Area)/(2*gamma)

#tau = (espesor*C_esp)/(2*(4*epsilon*sigma*(Tamb**3) +h))
#gamma =

caliente = experimento('/home/marco/Documents/fac/labo4/vacio/', claves=['calentar', '.txt'])

def DT_up(t,tau,A):
    return A*(1-np.exp(-t/tau))

def DT_up_sin(t,tau):
    return A*(1-np.exp(-t/tau))

def trim(df):
    Tinicial = df['Temperatura'].iloc[0]
    _ = df[df['Temperatura'] >= Tinicial + 2.]
    _.index = pd.RangeIndex(len(_.index))
    return _, Tinicial

for arch in caliente:
    print(arch)
    medicion = caliente.cargar_pd(arch)
    medicion, Tinicial = trim(medicion)
    y = medicion['Temperatura']
    t = medicion['Tiempo']
    Tfinal = y.iloc[-1]

    gmodel = Model(DT_up)
    result = gmodel.fit(y, t=t , A=Tfinal - Tinicial, tau=300)
    print(result.fit_report())
    plt.plot(t, result.best_fit)

    # A = Tfinal
    # gmodel = Model(DT_up_sin)
    # result = gmodel.fit(y, t=t, tau=300)
    # print(result.fit_report())
    # plt.plot(t, result.best_fit)

    plt.plot(t,y,'.')
    plt.title(caliente.titular(arch))
    plt.show()

    # plt.savefig(arch + '.png', dpi=300)
    plt.clf()


frio = experimento('/home/marco/Documents/fac/labo4/vacio/', claves=['apagar', '.txt'])
# def DT_down(t,tau,A):
#     A*np.exp(-t/tau)

