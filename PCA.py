import numpy as np
import matplotlib.pyplot as plt

datos = open('DatosBancoMundial5.csv','r')

txt= datos.readlines()

#filas-variables
fila1 = txt[1].split(',')
fila2 = txt[2].split(',')
fila3 = txt[3].split(',')
fila4 = txt[4].split(',')
fila5 = txt[5].split(',')
#fila 3 y 4 contienen una coma dentro del texto
fil1 = fila1[4:]
fil2 = fila2[4:]
fil3 = fila3[5:]
fil4 = fila4[5:]
fil5 = fila5[4:]

#Para convertir a flotante los miembros de la lista
c=0
var1=[]
var2=[]
var3=[]
var4=[]
var5=[]
while c<len(fil1):
	var1.append(float(fil1[c]))
	var2.append(float(fil2[c]))
	var3.append(float(fil3[c]))
	var4.append(float(fil4[c]))
	var5.append(float(fil5[c]))
	c+=1

#Para poder hacer operaciones con los datos, deben ser arrays
totTaxRate=np.array(var1)
cbStart=np.array(var2)
unFem=np.array(var3)
unMan=np.array(var4)
ratFemMan=np.array(var5)

#Normalizacion de los datos
totTaxRate = (totTaxRate - np.mean(totTaxRate))/np.std(totTaxRate)
cbStart = (cbStart - np.mean(cbStart))/np.std(cbStart)
unFem = (unFem - np.mean(unFem))/np.std(unFem)
unMan = (unMan - np.mean(unMan))/np.std(unMan)
ratFemMan = (ratFemMan - np.mean(ratFemMan))/np.std(ratFemMan)

#Grafica de los datos
plt.plot(totTaxRate,'r',label='Total tax rate')
plt.plot(cbStart,'g',label='Cost of business start-up procedures')
plt.plot(unFem,'c',label='Unemploymen, female')
plt.plot(unMan,'b',label='Unemploymen, male')
plt.plot(ratFemMan,'k',label='Ratio of female to male force participation')
plt.legend(loc=0)
plt.title('Datos Banco Mundial')
plt.savefig('ExploracionDatos.pdf')
plt.close()

#Calculo de la matriz de covarianza
matrizDat = [totTaxRate,cbStart, unFem, unMan, ratFemMan]
matrizDatos = np.transpose(matrizDat)
#se crea una matriz NxN (N el numero de variables)
a=(len(matrizDatos[0]),len(matrizDatos[0]))
MatrizCov=np.ones(a)
for i in range(len(matrizDatos[0])):
	for j in range(len(matrizDatos[0])):
		cov=0
		k=0
		while k< len(matrizDatos):
			cov+= ((matrizDatos[k][i]- matrizDatos[:,i].mean())*(matrizDatos[k][j]- matrizDatos[:,j].mean()))/(len(matrizDatos)-1)
			k+=1
		MatrizCov[i][j]= cov

#Valores y vectores propios
eigVal, eigVect = np.linalg.eig(MatrizCov)

a= eigVect[:,0]
b= eigVect[:,1]

print "El componente principal es:",a,",el segundo componente principal es:", b

#proyeccion datos en sistema de referencia de las 2 PCA
Ref_CompPrincipales = np.dot(np.transpose(eigVect), np.transpose(matrizDatos))
#Grafica con PCA
plt.scatter(Ref_CompPrincipales[0,:], Ref_CompPrincipales[1,:], c='c')
plt.xlabel('Componente Principal 1')
plt.ylabel('Componente Principal 2')
plt.title('Datos en sistema de referencia de las dos Componentes Principales')
plt.grid()
plt.savefig('PCAdatos.pdf')
plt.close()

#Grafica con variables agrupadas
fig = plt.figure()
ax= fig.add_subplot(111)
ax.scatter(a[0],b[0],c='r',s=80,marker='^', label='Total tax rate')
ax.scatter(a[1],b[1],c='g',s=80,label='Cost of business start-up procedures')
ax.scatter(a[2],b[2],c='c',s=80,marker='^',label='Unemploymen, female')
ax.scatter(a[3],b[3],c='b',s=80,label='Unemploymen, male')
ax.scatter(a[4],b[4],c='k',s=80,marker='^',label='Ratio of female to male force participation')
ax.legend(loc=0)
ax.annotate('Variables relacionadas(1)', xy=(0.07, 0.7), xytext =(0.16,0.6), arrowprops= dict(facecolor='black', shrink=0.05))
ax.annotate('Variables relacionadas(2)', xy=(0.65, -0.01), xytext =(0.2,0.085), arrowprops= dict(facecolor='black', shrink=0.05))
ax.set_xlabel('Componente Principal 1')
ax.set_ylabel('Componente Principal 2')
ax.set_title('Agrupacion de variables usando las componentes principales')
fig.savefig('PCAvariables.pdf')

print "Las variables que estan correlacionadas son: 1-'Total tax rate' con 'Cost of business start-up procedures' y 2-'Unemployment, female' con 'Unemployment, male'."


