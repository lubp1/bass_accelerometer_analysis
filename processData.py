import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pickle

data_path = r'C:\Users\lucas\Documents\Graduação\TFC\bass_accelerometer_analysis\data'
filename = 'yyz_8c5f0fe42d0d4e7192880824635be4c8.pkl'

# Lists to store sensors data
time = list()
acel = list()
acelX = list()
acelY = list()
acelZ = list()
plots = None

file = open(os.path.join(data_path, filename), 'rb')
data_dict = pickle.load(file)
file.close()

time = data_dict['timestamp']
acel = data_dict['resulting acceleration']
acelX = data_dict['X axis acceleration']
acelY = data_dict['Y axis acceleration']
acelZ = data_dict['Z axis acceleration']


# Apping an order 6 Butterworth filter
fs = 100
fc = 5  # Cut-off frequency of the filter
w = fc / (fs / 2) # Normalize the frequency
b, a = signal.butter(6, w, 'low')

acelFiltered = None
acelFiltered = signal.filtfilt(b, a, acel)
  
# Changing t0 to 0
time = (np.array(time) - time[0])*1e-3


# Resulting aceleration
plt.figure()
plt.plot(time, acel)
plt.plot(time, acelFiltered, linewidth=2)
plt.legend(('Dado bruto', 'Dado filtrado com Butterworth'))
plt.ylabel('Aceleração (m/s2)')
plt.xlabel('Tempo (s)')
plt.title('Aceleração x Tempo')

# Aceleration on 3 axis
plt.figure()
plt.plot(time, acelX)
plt.plot(time, acelY)
plt.plot(time, acelZ)
plt.legend(('Aceleração em X', 'Aceleração em Y', 'Aceleração em Z'))
plt.ylabel('Aceleração (m/s2)')
plt.xlabel('Tempo (s)')
plt.title('Aceleração x Tempo')

#%% Processing 

# Cut arrays according to audio start/end
t0_segment = 0.91
tf_segment = 24.2

new_indexes = np.where(time > t0_segment)[0]

new_time = time[new_indexes]
new_acel = np.array(acel)[new_indexes]
new_acelX = np.array(acelX)[new_indexes]
new_acelY = np.array(acelY)[new_indexes]
new_acelZ = np.array(acelZ)[new_indexes]

new_indexes = np.where(new_time < tf_segment)[0]

new_time = new_time[new_indexes]
new_acel = new_acel[new_indexes]
new_acelX = new_acelX[new_indexes]
new_acelY = new_acelY[new_indexes]
new_acelZ = new_acelZ[new_indexes]

plt.figure()
plt.plot(time, acel)
plt.plot(new_time, new_acel)
plt.legend(('Complete data', 'Segmented data'))
plt.ylabel('Acceleration (m/s2)')
plt.xlabel('Time (s)')
plt.title('Aceleration x Time - Segmenting')

#%% Add info to data dict and save to file

data_path = r'C:\Users\lucas\Documents\Graduação\TFC\bass_accelerometer_analysis\data\Processed data'

data_dict['Sync time (s)'] = new_time - new_time[0]
data_dict['Sync resulting acceleration'] = new_acel
data_dict['Sync X axis acceleration'] = new_acelX
data_dict['Sync Y axis acceleration'] = new_acelY
data_dict['Sync Z axis acceleration'] = new_acelZ

file = open(os.path.join(data_path, filename), 'wb')
pickle.dump(data_dict, file)
file.close()
