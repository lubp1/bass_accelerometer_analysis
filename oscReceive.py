# Import needed modules from osc4py3
from osc4py3.as_eventloop import *
from osc4py3 import oscmethod as osm
import json
import uuid
import sys
import csv
import math
import os
import pickle

music = 'Someday - The Strokes'
technique = 'picked'
filename = 'someday'

def handlerfunction(address, data):
    j = {'address' : address, 'data': data}
    print(json.dumps(j))
    file = open(filename + '.dat', 'a')
    file.write(json.dumps(j) + "\n")
    file.close()
    pass
print('iniciano o sistema\n')

unique_filename = str(uuid.uuid4().hex)
fname =  "data/" + filename + "_" + unique_filename + ".pkl"
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
    data_dict = dict()
    data_dict['technique'] = technique
    data_dict['music'] = music
    data_dict['resulting acceleration'] = list()
    data_dict['X axis acceleration'] = list()
    data_dict['Y axis acceleration'] = list()
    data_dict['Z axis acceleration'] = list()
    data_dict['timestamp'] = list()

    # load data from .dat file
    file = open(filename + '.dat', 'r')
    data = file.read()
    file.close()
    jsons = data.split('\n')
    jsons.pop()

    for i in jsons:
        json_data = json.loads(i)['data']

        if jsons.index(i) == 0:
            t0 = json_data[3]

        res = math.sqrt((json_data[0])**2 + (json_data[1])**2 + (json_data[2])**2)
        data_dict['resulting acceleration'].append(res)
        data_dict['X axis acceleration'].append(json_data[0])
        data_dict['Y axis acceleration'].append(json_data[1])
        data_dict['Z axis acceleration'].append(json_data[2])
        data_dict['timestamp'].append(json_data[3] - t0)

    file = open(fname, 'wb')
    pickle.dump(data_dict, file)
    file.close()

    os.remove(filename + '.dat')
    print('\nArquivo gerado com sucesso: ' + fname)
# Properly close the system.
    osc_terminate()