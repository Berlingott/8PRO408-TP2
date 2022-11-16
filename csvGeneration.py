from featureExtraction import extract_features
import math
import os
import pandas as pd
from scipy.io import wavfile
import shutil

sentences = [f'cc-{str(number).zfill(2)}' for number in range(1, 40)]
time_window_length = 500
overlap_length = 400
non_overlap_length = time_window_length - overlap_length
x_data = []
y_data = []
label_data = []
total_time = 0

def convert_to_csv():
    print('Converting WAV files to CSV.')
    # Makes sure we scroll through all the relevant folders.
    for person in [file for file in os.listdir('./RawData/') if os.path.isdir(f'./RawData/{file}')]:
        # Browse the WAV files
        for sentence in sentences:
            # Source code for the following: https://github.com/Lukious/wav-to-csv/blob/master/wav2csv.py
            # Used to convert a WAV file into a CSV file.

            _, data = wavfile.read(f'./RawData/{person}/wav/{sentence}.wav')  # The first rejected element is the rate, which is always 16kHz

            recording = pd.DataFrame(data)
            recording.columns = ['frequency']
            recording.to_csv(f'./RawData/{person}/wav/{sentence}.csv', index=False)


def convert_to_csv_with_quarters():
    print('Converting WAV files to CSV files with four columns.')
    # Makes sure we scroll through all the relevant folders.
    for person in [file for file in os.listdir('./RawData/') if os.path.isdir(f'./RawData/{file}')]:
        # Browse the WAV files
        for sentence in sentences:
            # Source code for the following: https://github.com/Lukious/wav-to-csv/blob/master/wav2csv.py
            # Used to convert a WAV file into a CSV file.

            _, data = wavfile.read(f'./RawData/{person}/wav/{sentence}.wav')  # The first rejected element is the rate, which is always 16kHz

            recording = pd.DataFrame(data)
            quarter_number = math.floor(recording.shape[0]/4)
            excedent = recording.shape[0] % 4
            # We drop the beginning of the recordings because they are usually silent.
            recording = recording.drop([index for index in range(excedent)])
            recording = recording.reset_index(drop=True)

            final = pd.DataFrame()

            final['Q1'] = recording.squeeze().iloc[:quarter_number]
            recording = recording.drop([index for index in range(quarter_number)])
            recording = recording.reset_index(drop=True)
            final['Q2'] = recording.squeeze().iloc[:quarter_number]
            recording = recording.drop([index for index in range(quarter_number)])
            recording = recording.reset_index(drop=True)
            final['Q3'] = recording.squeeze().iloc[:quarter_number]
            recording = recording.drop([index for index in range(quarter_number)])
            recording = recording.reset_index(drop=True)
            final['Q4'] = recording.squeeze().iloc[:quarter_number]

            os.makedirs(os.path.dirname(f'./Quarters/{sentence}/{person}.csv'), exist_ok=True)
            final.to_csv(f'./Quarters/{sentence}/{person}.csv', index=False)


def one_csv_per_person():
    print('Merging the CSV files into one file per person.')
    # Scrolls through each person
    for person in [file for file in os.listdir('./RawData/') if os.path.isdir(f'./RawData/{file}')]:
        # Browse the sentence CSV files
        final = pd.DataFrame()
        for sentence in sentences:
            column = pd.read_csv(f'./RawData/{person}/wav/{sentence}.csv')
            column = column.squeeze(axis=0)
            final[sentence] = column
        final.to_csv(f'./RawData/{person}/person.csv', index=False)




def generate_group_csv():
    print('Generating an overview file of the persons\' categorical values.')
    persons = list()

    # Makes sure we scroll through all the relevant folders: starts with "Personne" and is actually a folder.
    for person in [file for file in os.listdir('./RawData/') if os.path.isdir(f'./RawData/{file}')]:

        with open(f'./RawData/{person}/etc/README', 'r') as input:
            # Remove all line returns
            text = ' '.join(input.readlines())
            # Transform the text into a list of tokens
            text = text.split()
            # Find the index of "Gender:" and get the gender from the next value
            gender = text[text.index('Gender:') + 1]
            # Find the index of "Language:" and get the language from the next value
            try:
                language_tmp = text[text.index('Language:') + 1]
            except ValueError:
                language_tmp = 'Unknown'
            language = language_tmp

        person = {
            'ID': person,
            'Gender': gender,
            'Language': language
        }

        persons.append(person)

    persons = pd.DataFrame(persons)
    persons.to_csv('./RawData/persons.csv', index=False)


def clean_data():
    print('Creating a clean folder.')
    persons = [person for person in os.listdir('./RawData/') if os.path.isdir(f'./RawData/{person}')]
    for person in persons:
        os.makedirs(os.path.dirname(f'./CleanData/{person}/person.csv'), exist_ok=True)
        shutil.copy(f'./RawData/{person}/person.csv', f'./CleanData/{person}/person.csv')
        for sentence in sentences:
            shutil.copy(f'./RawData/{person}/wav/{sentence}.csv', f'./CleanData/{person}/{sentence}.csv')


if __name__ == '__main__':
    convert_to_csv()

    convert_to_csv_with_quarters()

    # one_csv_per_person()

    # generate_group_csv()

    # clean_data()

    print('We are the champions 🎶')