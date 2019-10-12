


from __future__ import division, unicode_literals, print_function, absolute_import

import time

import visa

import matplotlib.pyplot as plt
#print(__doc__)

# Este string determina el intrumento que van a usar.
# Lo tienen que cambiar de acuerdo a lo que tengan conectado.

osciloscopio = 'USB0::0x0699::0x0363::C065092::INSTR'


rm1 = visa.ResourceManager()

osci = rm1.open_resource(osciloscopio)

# Pide indentificacion
print(osci.query('*IDN?'))


#######################################################################

"""
Generador de funciones Tektronix AFG 3021B
Manual U (web): https://github.com/hgrecco/labosdf-bin/raw/master/manuals/TektronixAFG3000.pdf
Manual P (web): https://github.com/hgrecco/labosdf-bin/raw/master/manuals/TektronixAFG3000_p.pdf
Manual U (local): \\Srvlabos\manuales\Tektronix\AFG3012B (M Usuario).pdf
Manual P (local): \\Srvlabos\manuales\Tektronix\AFG3012B (Prog Manual).pdf
"""

import numpy as np



# Este string determina el intrumento que van a usar.
# Lo tienen que cambiar de acuerdo a lo que tengan conectado.

generador = 'USB0::0x0699::0x0346::C033248::INSTR'

rm2 = visa.ResourceManager()

# Abre la sesion VISA de comunicacion
fungen = rm2.open_resource(generador)

print(fungen.query('*IDN?'))



#######################################################################



# tiempo = float(input("Introduzca el tiempo a medir: "))
#frec = float(input("Introduzca la frecuencia de muestreo en Hz: "))
#frec1 = float(input("Introduzca la frecuencia minima en Hz: (50080): "))
#frec2 = float(input("Introduzca la frecuencia maxima en Hz: (50370): "))
#paso = float(input("Introduzca el paso en Hz: "))
frec = 99
frec1 = 150152
frec2 = 150164
paso = 1

datos=[]
setup = osci.query('WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;')
print('setup:')
print(setup)
# Rampa lineal de frequencias
frecuencias = np.linspace(frec1, frec2, int((frec2-frec1)/paso)+1)

for freq in frecuencias:
    fungen.write('SOUR1:FREQ %f' % freq)
    time.sleep(0.3)	
    print('mido')
#    fungen.write('FREQ %f' % freq)
#    #    fprintf(osci, 'MEASUrement:IMMed:CH1')
#    amplitudCh1 = float(osci.query('MEASUrement:IMMed:TYPe CRMs;SOU?'))
#    #    fprintf(osci, 'MEASUrement:IMMed:CH2')
#    amplitudCh2 = float(osci.query('MEASUrement:IMMed:TYPe CRMs;SOU?')) 
#    Trans= amplitudCh1/amplitudCh2
#    fCh1Ch2T= [freq, amplitudCh1,amplitudCh2,Trans]
#    datos.append(fCh1Ch2T)
        #elijo la frecuencia del generador

#    time.sleep(0.01)
    #Elijo el canal 1 del osciloscopio
#    osci.write('DATA:SOURCE CH1')
    #Le pido al osciloscopio los datos del canal 1

    osci.write('MEASUrement:IMMed:SOURCE CH1')
    osci.write('MEASUrement:IMMed:TYPe CRMs')
    amplitudCh1 = float(osci.query('MEASUrement:IMMed:VALue?'))
    
    osci.write('MEASUrement:IMMed:SOURCE CH2')
    osci.write('MEASUrement:IMMed:TYPe CRMs')
    amplitudCh2 = float(osci.query('MEASUrement:IMMed:VALue?'))
    try:
        Trans= amplitudCh2/amplitudCh1
    except ZeroDivisionError:
        Trans = np.NaN
    fCh1Ch2T= [freq, amplitudCh1,amplitudCh2,Trans]
    datos.append(fCh1Ch2T)
    print(f'datos: {fCh1Ch2T}')
	

print(datos)

medicion = np.array(datos)

nombre = input('nombre del archivo:')

np.savetxt(nombre, medicion)
#np.savetxt(nombre + 'setup',setup)

#import matplotlib.pyplot as plt
#
#
plt.plot(medicion[:,0], medicion[:,2],'.')
plt.show()

# A = np.loadtxt("nombredelarchivo.txt")   <--- Esta linea es para cargar el archivo con los datos por si se lo quiere manipular desde Python despues de medir.


fungen.close()
osci.close()


 