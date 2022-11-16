import os
import pandas as pd
from scipy.io import wavfile

# This file converts the WAV files to CSV files ready for analysis
# using the code from the teacher's provided example.

# From a0007 to a0016
sentences = [f'a{str(number).zfill(4)}' for number in range(7, 17)]

def convert_to_csv():
    print('Converting WAV files to CSV files.')
    # Makes sure we scroll through all the relevant folders.
    for person in [file for file in os.listdir('./RawData/') if os.path.isdir(f'./RawData/{file}')]:
        # Browse the WAV files
        for sentence in sentences:
            # Source code for the following: https://github.com/Lukious/wav-to-csv/blob/master/wav2csv.py
            # Used to convert a WAV file into a CSV file.
            _, data = wavfile.read(f'./RawData/{person}/wav/{sentence}.wav')  # The first rejected element is the rate, which is always 16kHz

            recording = pd.DataFrame(data)
            recording.columns = ['amp']

            os.makedirs(os.path.dirname(f'./CleanData/{sentence}/{person}.csv'), exist_ok=True)
            recording.to_csv(f'./CleanData/{sentence}/{person}.csv', index=False)

def convert_to_amp_freq():
    print('Converting the audio signal to amplitudes and frequencies.')
    # Makes sure we scroll through all the relevant folders.
    for person in [file for file in os.listdir('./RawData/') if os.path.isdir(f'./RawData/{file}')]:
        # Browse the WAV files
        for sentence in sentences:
            # Source code for the following: https://github.com/Lukious/wav-to-csv/blob/master/wav2csv.py
            # Used to convert a WAV file into a CSV file.
            _, data = wavfile.read(f'./RawData/{person}/wav/{sentence}.wav')  # The first rejected element is the rate, which is always 16kHz

            recording = pd.Series(data)
            previous_sample = None
            count = 0
            amplitudes = list()
            frequencies = list()
            ascending = True

            for sample in recording:
                count = count + 1
                if previous_sample is None:
                    previous_sample = sample
                    continue
                if (previous_sample > sample and ascending == True) or (previous_sample < sample and ascending == False):
                    amplitudes.append(abs(previous_sample))
                    if ascending == True:
                        frequencies.append(16000/count)
                        count = 0
                    else:
                        frequencies.append(frequencies[-1])
                    ascending = not ascending
                previous_sample = sample

            # Make sure we don't keep a partial half-cycle at the beginning
            if recording.loc[0] > recording.loc[1]:
                amplitudes.pop(0)
                frequencies.pop(0)

            # Make the two columns of equal length
            if len(amplitudes) > len(frequencies):
                amplitudes.pop(0)

            conversion = pd.DataFrame()
            conversion['amp'] = amplitudes
            conversion['freq'] = frequencies

            os.makedirs(os.path.dirname(f'./AmpFreq/{sentence}/{person}.csv'), exist_ok=True)
            conversion.to_csv(f'./AmpFreq/{sentence}/{person}.csv', index=False)


if __name__ == '__main__':
    convert_to_csv()
    convert_to_amp_freq()