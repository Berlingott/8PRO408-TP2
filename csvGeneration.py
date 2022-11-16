import os
import pandas as pd
from scipy.io import wavfile

# This file converts the WAV files to CSV files ready for analysis
# using the code from the teacher's provided example.

# From a0007 to a0016
sentences = [f'a{str(number).zfill(4)}' for number in range(7, 17)]

# Using a window length that is too short causes sets of values
# that are too similar. This in turn generates NaNs for kurtosis
# and skewness. The dimentionality reduction tool does not support
# NaNs. For that reason a wider window needs to be applied.
time_window_length = 500
overlap_length = 400
non_overlap_length = time_window_length - overlap_length
x_data = []
y_data = []
label_data = []
total_time = 0

def convert_to_csv():
    print('Converting WAV files to CSV files with four columns.')
    # Makes sure we scroll through all the relevant folders.
    for person in [file for file in os.listdir('./RawData/') if os.path.isdir(f'./RawData/{file}')]:
        # Browse the WAV files
        for sentence in sentences:
            # Source code for the following: https://github.com/Lukious/wav-to-csv/blob/master/wav2csv.py
            # Used to convert a WAV file into a CSV file.
            _, data = wavfile.read(f'./RawData/{person}/wav/{sentence}.wav')  # The first rejected element is the rate, which is always 16kHz

            recording = pd.DataFrame(data)

            os.makedirs(os.path.dirname(f'./CleanData/{sentence}/{person}.csv'), exist_ok=True)
            recording.to_csv(f'./CleanData/{sentence}/{person}.csv', index=False)

if __name__ == '__main__':
    convert_to_csv()