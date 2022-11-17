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
result['frequency (kHz)'] = frqLabel[:(d-1)]/1000 # Convert frequencies from Hz to kHz
result['amplitude'] = abs(c[:(d-1)])

fig = px.line(result, x='frequency (kHz)', y='amplitude')

# Works only when installing kaleido as "pip install kaleido==0.2.1.post1"
# Discussion: https://github.com/plotly/Kaleido/issues/134
fig.write_image("fourier.png")

result = result.sort_values(by='amplitude', ascending=False)
result = result.reset_index()

amplitude1 = result['amplitude'].loc[0]
frequency1 = result['frequency (kHz)'].loc[0]
amplitude2 = result['amplitude'].loc[1]
frequency2 = result['frequency (kHz)'].loc[1]
amplitude3 = result['amplitude'].loc[2]
frequency3 = result['frequency (kHz)'].loc[2]

print('The stats for the three biggest peeks are:')
print(f'    - amp1:     {amplitude1}')
print(f'    - freq1:    {frequency1}')
print(f'    - amp2:     {amplitude2}')
print(f'    - freq2:    {frequency2}')
print(f'    - amp3:     {amplitude3}')
print(f'    - freq3:    {frequency3}')