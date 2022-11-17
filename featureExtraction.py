import numpy as np
import pandas as pd
from scipy import stats
from scipy.fftpack import fft


def extract_min(data):

    min_values = np.min(data, axis=0)

    return min_values

def extract_max(data):

    max_values = np.max(data, axis=0)

    return max_values

def extract_mean(data):

    mean_values = np.mean(data, axis=0)

    return mean_values


def extract_std(data):

    std_values = np.std(data, axis=0)

    return std_values

def extract_skewness(data):

    skewness_values = stats.skew(data, axis=0)

    return skewness_values


def extract_kurtosis(data):

    kurtosis_values = stats.kurtosis(data, axis=0)

    return kurtosis_values

def extract_difference(data):

    data = pd.DataFrame(data)
    biggest_diffs = list()

    for column in data:
        biggest_diff = 0
        last_datum = None
        for datum in data[column]:
            if last_datum is not None:
                difference = abs(datum - last_datum)
                if difference > biggest_diff:
                    biggest_diff = difference
            last_datum = datum
        biggest_diffs.append(biggest_diff)

    return np.array(biggest_diffs)

def extract_sum(data):

    sum_values = np.sum(data, axis=0)

    return sum_values

def extract_slope(data):
    data = pd.DataFrame(data)
    slope_values = list()

    for column in data:
        values = data[column].to_list()
        slope, _ = np.polyfit(range(0, len(values)), values, 1)
        slope_values.append(slope)

    return np.array(slope_values)

def extract_count(data):
    data = pd.DataFrame(data)
    count_values = list()
    
    for column in data:
        column_df = pd.DataFrame(data[column])
        count_values.append(column_df.groupby(column)[column].count().max())

    return np.array(count_values)

def extract_fourier(data):
    data = pd.DataFrame(data)
    frequency1_values = list()
    amplitude1_values = list()
    frequency2_values = list()
    amplitude2_values = list()
    frequency3_values = list()
    amplitude3_values = list()

    for column in data:
        # Source for this Fourier transformation: https://stackoverflow.com/a/23378284
        a = np.array(data[column]) # load the data
        b = [ele/2**16 for ele in a] # this is 16-bit track, b is now normalized on [-1,1)
        c = fft(b) # calculate fourier transform (complex numbers list)
        d = int(len(c)/2) # you only need half of the fft list (real signal symmetry)
        k = np.arange(len(a))
        T = len(data)/16000 # where 16,000 is the sampling frequency
        frqLabel = k/T
        spectrum = pd.DataFrame()
        spectrum['Frequency'] = frqLabel[:(d-1)]
        spectrum['Amplitude'] = abs(c[:(d-1)])

        spectrum = spectrum.sort_values(by='Amplitude', ascending=False)
        spectrum = spectrum.reset_index()

        amplitude1 = spectrum['Amplitude'].loc[0]
        frequency1 = spectrum['Frequency'].loc[0]
        amplitude2 = spectrum['Amplitude'].loc[1]
        frequency2 = spectrum['Frequency'].loc[1]
        amplitude3 = spectrum['Amplitude'].loc[2]
        frequency3 = spectrum['Frequency'].loc[2]

        amplitude1_values.append(amplitude1)
        frequency1_values.append(frequency1)
        amplitude2_values.append(amplitude2)
        frequency2_values.append(frequency2)
        amplitude3_values.append(amplitude3)
        frequency3_values.append(frequency3)

    return np.array(frequency1_values), np.array(amplitude1_values), np.array(frequency2_values), np.array(amplitude2_values), np.array(frequency3_values), np.array(amplitude3_values)
    

def extract_features(data):

    tmp = extract_min(data)
    tmp = np.append(tmp, extract_max(data))
    tmp = np.append(tmp, extract_mean(data))
    tmp = np.append(tmp, extract_std(data))
    tmp = np.append(tmp, extract_skewness(data))
    tmp = np.append(tmp, extract_kurtosis(data))
    tmp = np.append(tmp, extract_difference(data))
    tmp = np.append(tmp, extract_sum(data))
    tmp = np.append(tmp, extract_slope(data))
    tmp = np.append(tmp, extract_count(data))
    freq1, amp1, freq2, amp2, freq3, amp3 = extract_fourier(data)
    tmp = np.append(tmp, freq1)
    tmp = np.append(tmp, amp1)
    tmp = np.append(tmp, freq2)
    tmp = np.append(tmp, amp2)
    tmp = np.append(tmp, freq3)
    tmp = np.append(tmp, amp3)

    return tmp, ["min", "max", "mean", "std", "skew", "kurt", "diff", "sum", "slope", "count", "freq1", "amp1", "freq2", "amp2", "freq3", "amp3"]