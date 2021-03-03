import csv
import sys
import json
import math
import operator
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal



# coluna do CSV de cada dado
sensorAddress = 0
acres = 1
acx = 2
acy = 3
acz = 4
timestamp = 5
# roll = 6
# pitch = 7
# gyx = 8
# gyy = 9
# gyz = 10

filename = 'data/test_e7e86c73f2f94376be79966d393f49cb.csv'


# Listas para os dados de todos os sensores
time = list()
acel = list()
acelX = list()
acelY = list()
acelZ = list()
# rollAngle = [[],[], [], []]
# pitchAngle = [[],[], [], []]
# acelFiltered = [[],[], [], []]
# gyroX = [[],[], [], []]
# gyroY = [[],[], [], []]
# gyroZ = [[],[], [], []]
maxsensor = 0 # numero do maior id de sensor
plots = None

# Lendo o CSV e criando as listas para cada sensor
with open(filename,'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    sortedlist = sorted(plots, key=operator.itemgetter(sensorAddress)) 
    for row in sortedlist:
        if row[acres] != 'nan':
            time.append(float(row[timestamp]))
            acel.append(float(row[acres]))
            acelX.append(float(row[acx]))
            acelY.append(float(row[acy]))
            acelZ.append(float(row[acz]))
        # rollAngle[int(row[0][1])].append(float(row[roll]))
        # pitchAngle[int(row[0][1])].append(float(row[pitch]))
        # gyroX[int(row[0][1])].append(float(row[gyx]))
        # gyroY[int(row[0][1])].append(float(row[gyy]))
        # gyroZ[int(row[0][1])].append(float(row[gyz]))


# Calculando o sinal da aceleracao resultante filtrado por um filtro Butterworth de ordem 6
fs = 100
fc = 5  # Cut-off frequency of the filter
w = fc / (fs / 2) # Normalize the frequency
b, a = signal.butter(6, w, 'low')

acelFiltered = None
acelFiltered = signal.filtfilt(b, a, acel)
    

# Fazendo todos os tempo comecarem em 0:
time = (np.array(time) - time[0])*1e-3


# print("Quantas comparações de pares de sensores serão feitas?(ex: '1')")
# numsensores = (input().split("\n")[0])
# numsensores = int(numsensores)
# i = 0
# sensores = [[],[]]
# if (numsensores>0):
#     print("Quais sensores serão comparados?(ex: '0 1') Pressione enter caso não queira comparar sensores.")
#     while (i<numsensores):
#         sensor = (input().split("\n")[0]).split(' ')
#         sensores[0].append(sensor[0])
#         sensores[1].append(sensor[1])
#         i += 1


# Plotando o grafico de todos os dados para cada sensor
plt.figure()
plt.plot(time, acel)
plt.plot(time, acelFiltered, linewidth=2)
plt.legend(('Dado bruto', 'Dado filtrado com Butterworth'))
plt.ylabel('Aceleração (g)')
plt.title('Aceleração e Ângulo x Amostra - ' + (((filename).split('/')[1]).split('_')[0]).split('.')[0])

# Grafico da aceleracao nos tres eixos
plt.figure()
plt.plot(time, acelX)
plt.plot(time, acelY)
plt.plot(time, acelZ)
plt.legend(('Aceleração em X', 'Aceleração em Y', 'Aceleração em Z'))
plt.ylabel('Aceleração (g)')

# # Grafico da velocidade angular nos tres eixos
# plt.subplot(4,1,3)
# plt.plot(acelX[i])
# plt.plot(time[i], acelY[i])
# plt.plot(time[i], acelZ[i])
# plt.legend(('Giro em X', 'Giro em Y', 'Giro em Z'))
# plt.ylabel('Giro (graus/s)')

# # Grafico dos angulos de roll e pitch
# plt.subplot(4,1,4)
# plt.plot(time[i],rollAngle[i])
# plt.plot(time[i],pitchAngle[i])
# plt.legend(('Ângulo de Roll', 'Ângulo de Pitch'))
# plt.xlabel('Tempo (s)')
# plt.ylabel('Ãngulo (graus)')

# Salvando a figura com os graficos
plt.savefig((filename).split('.csv')[0] + '.png')

# # Comparando o dado de dois sensores
# i = 0
# while (i<numsensores):
#     plt.figure()
#     plt.plot(time[int(sensores[0][i])], acelFiltered[int(sensores[0][i])], linewidth=2)
#     plt.ylabel('Aceleração (g)')
#     plt.title('Comparação entre os sensores ' + str(sensores[0][i]) + ' e ' + str(sensores[1][i]) + ' - ' + (((sys.argv[1]).split('/')[1]).split('_')[0]).split('.')[0])
#     plt.plot(time[int(sensores[1][i])], acelFiltered[int(sensores[1][i])], linewidth=2)
#     plt.legend(('Sensor ' + str(sensores[0][i]), 'Sensor ' + str(sensores[1][i])))
#     plt.ylabel('Aceleração (g)')
#     plt.savefig((sys.argv[1]).split('.csv')[0] + '_comparacao_' + str(sensores[0][i]) + 'e' + str(sensores[1][i]) + '.png')
#     i += 1
# plt.show()

