import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
from scipy.fftpack import fft, fftfreq, ifft



#Lectura archivos wav
rateDo, dataDo = wav.read('Do.wav')
rateSol, dataSol = wav.read('Sol.wav')


#Rango para probar implementaciones
#dataDo = dataDo[0:1000]
#dataSol = dataSol[0:1000]

NDo= len(dataDo)
NSol = len(dataSol)
freqDo = fftfreq(NDo, 1.0/rateDo)
freqSol = fftfreq(NSol, 1.0/rateSol)


#Mi implementacion para la transformada de fourier
def transformada(datosNot):
	N=len(datosNot)
	Nf=float(N)
	datosNota = np.copy(datosNot)
	n=0
	transp=[]
	while n<N:
		trans=0
		k=0
		while k<N:
			trans += datosNota[k]*np.exp(-1j*2.0*np.pi*k*(n/Nf))
			k+=1
		transp.append(trans)
        	n+=1
	return np.asarray(transp)

#Transformadas
transformadaDo= transformada(dataDo)
transformadaSol= transformada(dataSol)

#Funcion que filtra la frecuencia con mayor amplitud
def funFiltroMAX(freqNota, transformadaNota):
	tr = np.copy(transformadaNota)
	pvalmax= np.argmax(abs(tr))
	pvalmaxNeg = np.where(freqNota ==-freqNota[pvalmax])[0][0]
	dt = 40
	tr[pvalmax-dt:pvalmax+dt]=0
	tr[pvalmaxNeg-dt:pvalmaxNeg+dt]=0
	return np.asarray(tr)

FiltroMaxDo = funFiltroMAX(freqDo, transformadaDo)

#Elimina todas las frecuencias mayores a 1000 Hz
def funFiltroBajos( freqNotaa, transformadaNotaa, dataNota):
	trans =  np.copy(transformadaNotaa)
	N=len(dataNota)
	i=0
	while i<N:
		if abs(freqNotaa[i]) > 1000.0:
			trans[i]=0
		i+=1
	return np.asarray(trans)

FiltroBajosDo = funFiltroBajos(freqDo, transformadaDo, dataDo)

#Grafica con datos originales y aplicacion de los filtros
f, pl = plt.subplots(3, sharex = True, sharey = True)
pl[0].plot(freqDo,abs(transformadaDo),'c', label='Datos Originales')
pl[0].set_title('Grafica de operaciones con Do')
pl[0].legend(loc='upper right')
pl[1].plot(freqDo,abs(FiltroMaxDo),'g', label='Filtro para altos')
pl[1].legend(loc='upper right')
pl[2].plot(freqDo,abs(FiltroBajosDo),'m', label='Filtro para bajos (freq>1000Hz)')
pl[2].legend(loc='upper right')
f.text(0.5,0.04, 'Frecuencias (Hz)', ha = 'center')
f.text(0.04,0.5, 'Amplitudes', va='center', rotation='vertical')
plt.savefig('DoFiltros.pdf')
plt.show()
plt.close()



#Modificar frec. fundamental de Do(260Hz) a la de Sol(391Hz)
freqFundDo = 260.0
freqFundSol = 391.0
rateNuevoDo = rateDo*(freqFundSol)/freqFundDo
freqNuevaDo = fftfreq(NDo, 1/rateNuevoDo)

#Comparacion nota modificada de Do con transformada de Sol 
plt.plot(freqSol, abs(transformadaSol), 'c', label='Transformada de Sol')
plt.plot(freqNuevaDo, abs(transformadaDo), 'k', label='Do modificada')
plt.xlim(-8000,8000)
plt.legend(loc=0)
plt.savefig('DoSol.pdf')
plt.show()

#DoSol
datDon = transformadaDo
datDon = np.asarray(ifft(datDon))
datDon = datDon.real
datDon.astype(np.float32)
wav.write("DoSol.wav", int(rateNuevoDo), datDon)


#Sin Picos
FiltroAltosDo = np.asarray(ifft(FiltroMaxDo))
FiltroAltosDo = FiltroAltosDo.real
FiltroAltosDo.astype(np.float32)
wav.write("Do_pico.wav", rateDo, FiltroAltosDo)


#Sin Bajos
FiltroBajosDo = np.asarray(ifft(FiltroBajosDo))
FiltroBajosDo = FiltroBajosDo.real
FiltroBajosDo.astype(np.float32)
wav.write("Do_pasabajos.wav", rateDo, FiltroBajosDo)





