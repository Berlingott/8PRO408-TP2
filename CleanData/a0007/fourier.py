import os
import numpy as np
import pandas as pd
import plotly.express as px
from scipy.fftpack import fft

data = pd.read_csv([file for file in os.listdir()][0])

# Source for this Fourier transformation: https://stackoverflow.com/a/23378284
a = np.array(data['pres']) # load the data
b = [ele/2**16 for ele in a] # this is 16-bit track, b is now normalized on [-1,1)
c = fft(b) # calculate fourier transform (complex numbers list)
d = int(len(c)/2) # you only need half of the fft list (real signal symmetry)
k = np.arange(len(a))
T = len(data)/16000 # where 16,000 is the sampling frequency
frqLabel = k/T

result = pd.DataFrame()
result['Frequency'] = frqLabel[:(d-1)]
result['Amplitude'] = abs(c[:(d-1)])

fig = px.line(result, x='Frequency', y='Amplitude')
fig.show()

print(result['Frequency'].loc[result['Amplitude'].idxmax(axis=0)])