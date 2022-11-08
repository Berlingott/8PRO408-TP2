import os
import pandas as pd
from scipy.io import wavfile


def convert_to_csv():
    # Makes sure we scroll through all the relevant folders.
    for person_folder in [folder for folder in os.listdir('./RawData/') if folder.startswith('Personne')]:
        for wav_file in [file for file in os.listdir(f'./RawData/{person_folder}/wav/') if file.endswith('.wav')]:

            # Source code for the following: https://github.com/Lukious/wav-to-csv/blob/master/wav2csv.py
            # Used to convert a WAV file into a CSV file.

            _, data = wavfile.read(f'./RawData/{person_folder}/wav/{wav_file}')  # The first rejected element is the rate, which is always 16kHz

            recording = pd.DataFrame(data)
            recording.to_csv(f'./RawData/{person_folder}/wav/{wav_file.removesuffix(".wav")}.csv', index=False)

if __name__ == '__main__':
    convert_to_csv()

    print('We are the champions 🎶')