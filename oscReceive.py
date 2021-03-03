# Import needed modules from osc4py3
from osc4py3.as_eventloop import *
from osc4py3 import oscmethod as osm
import json
import uuid
import sys
import csv
import math
import os

fescala = 8 # fundo de escala do acelerometro
fgiro = 2000 # fundo de escala do giroscopio
filename = 'data/test'

def handlerfunction(address, data):
    j = {'address' : address, 'data': data}
    print(json.dumps(j))
    file = open(filename + '.dat', 'a')
    file.write(json.dumps(j) + "\n")
    file.close()
    pass
print('iniciano o sistema\n')

unique_filename = str(uuid.uuid4().hex)
fname =  filename + "_" + unique_filename + ".csv"
# Start the system.
osc_startup()

print('iniciando o servidor\n')

# Make server channels to receive packets.
osc_udp_server("192.168.0.26", 9001, "servername")

print('servidor iniciado.\n')

# Associate Python functions with message address patterns, using default
# argument scheme OSCARG_DATAUNPACK.
osc_method("/*", handlerfunction, argscheme=osm.OSCARG_ADDRESS + osm.OSCARG_DATA)


try:
# Periodically call osc4py3 processing method in your event loop.
    while (1):
    # …
        osc_process()
    # …
except KeyboardInterrupt:
    with open(fname, 'w', newline='') as csvfile:
        file = open(filename + '.dat', 'r')
        data = file.read()
        file.close()
        jsons = data.split('\n')
        jsons.pop()
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)              
        for i in jsons:
            linha = json.loads(i)
            res = math.sqrt((linha["data"][0])**2 + (linha["data"][1])**2 + (linha["data"][2])**2)
            spamwriter.writerow([linha["address"], res, linha["data"][0], linha["data"][1], linha["data"][2], linha["data"][3]])
    os.remove(filename + '.dat')
    print('\nArquivo gerado com sucesso: ' + fname)
# Properly close the system.
    osc_terminate()