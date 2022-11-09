import os
import pandas as pd
from scipy.io import wavfile

sentence_list = ['a0003.wav', 'a0004.wav', 'a0005.wav', 'a0006.wav']

def convert_to_csv():
    # Makes sure we scroll through all the relevant folders: starts with "Personne" and is actually a folder.
    for person_folder in [file for file in os.listdir('./RawData/') if os.path.isdir(f'./RawData/{file}')]:
        # Browse the WAV files
        for wav_file in [file for file in os.listdir(f'./RawData/{person_folder}/wav/') if file in sentence_list]:

            # Source code for the following: https://github.com/Lukious/wav-to-csv/blob/master/wav2csv.py
            # Used to convert a WAV file into a CSV file.

            _, data = wavfile.read(f'./RawData/{person_folder}/wav/{wav_file}')  # The first rejected element is the rate, which is always 16kHz

            recording = pd.DataFrame(data)
            recording.to_csv(f'./RawData/{person_folder}/wav/{wav_file.removesuffix(".wav")}.csv', index=False)


def generate_group_csv():
    persons = list()

    # Makes sure we scroll through all the relevant folders: starts with "Personne" and is actually a folder.
    for person_folder in [file for file in os.listdir('./RawData/') if os.path.isdir(f'./RawData{file}')]:

        with open(f'./RawData/{person_folder}/etc/README', 'r') as input:
            # Remove all line returns
            text = ' '.join(input.readlines())
            # Transform the text into a list of tokens
            text = text.split()
            # Find the index of "Gender:" and get the gender from the next value
            gender = text[text.index('Gender:') + 1]
            # Find the index of "Language:" and get the language from the next value
            language = text[text.index('Language:') + 1]

        person = {
            'ID': person_folder,
            'Gender': gender,
            'Language': language
        }

        persons.append(person)

    persons = pd.DataFrame(persons)
    persons.to_csv(f'./RawData/persons.csv', index=False)

if __name__ == '__main__':
    convert_to_csv()

    generate_group_csv()

    print('We are the champions 🎶')