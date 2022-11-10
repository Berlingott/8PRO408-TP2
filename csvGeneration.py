import concurrent.futures
from featureExtraction import extract_features
import math
import multiprocessing
import os
import pandas as pd
import pickle
from scipy.io import wavfile
import shutil
import time

sentences = ['a0003', 'a0004', 'a0005', 'a0006']
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
    for person_folder in [file for file in os.listdir('./RawData/') if os.path.isdir(f'./RawData/{file}')]:
        # Browse the WAV files
        for sentence in sentences:
            # Source code for the following: https://github.com/Lukious/wav-to-csv/blob/master/wav2csv.py
            # Used to convert a WAV file into a CSV file.

            _, data = wavfile.read(f'./RawData/{person_folder}/wav/{sentence}.wav')  # The first rejected element is the rate, which is always 16kHz

            recording = pd.DataFrame(data)
            recording.columns = ['frequency']
            recording.to_csv(f'./RawData/{person_folder}/wav/{sentence}.csv', index=False)


def convert_to_csv_with_quarters():
    print('Converting WAV files to CSV files with four columns.')
    # Makes sure we scroll through all the relevant folders.
    for person_folder in [file for file in os.listdir('./RawData/') if os.path.isdir(f'./RawData/{file}')]:
        # Browse the WAV files
        for sentence in sentences:
            # Source code for the following: https://github.com/Lukious/wav-to-csv/blob/master/wav2csv.py
            # Used to convert a WAV file into a CSV file.

            _, data = wavfile.read(f'./RawData/{person_folder}/wav/{sentence}.wav')  # The first rejected element is the rate, which is always 16kHz

            recording = pd.DataFrame(data)
            quarter_number = math.floor(recording.shape[0]/4)
            excedent = recording.shape[0] % 4
            # We drop the beginning of the recordings because they are usually silent.
            recording.drop(index=recording.index[:excedent], axis=0, inplace=True)

            final = pd.DataFrame()
            final['Q1'] = recording.squeeze()[:quarter_number]
            recording.drop(index=recording.index[:quarter_number], axis=1, inplace=True)
            final['Q2'] = recording.squeeze()[:quarter_number]
            recording.drop(index=recording.index[:quarter_number], axis=1, inplace=True)
            final['Q3'] = recording.squeeze()[:quarter_number]
            recording.drop(index=recording.index[:quarter_number], axis=1, inplace=True)
            final['Q4'] = recording.squeeze()[:quarter_number]

            os.makedirs(os.path.dirname(f'./Quarters/{person_folder}/{sentence}.csv'), exist_ok=True)
            final.to_csv(f'./Quarters/{person_folder}/{sentence}.csv', index=False)


def one_csv_per_person():
    print('Merging the CSV files into one file per person.')
    # Scrolls through each person
    for person_folder in [file for file in os.listdir('./RawData/') if os.path.isdir(f'./RawData/{file}')]:
        # Browse the sentence CSV files
        final = pd.DataFrame()
        for sentence in sentences:
            column = pd.read_csv(f'./RawData/{person_folder}/wav/{sentence}.csv')
            column = column.squeeze(axis=0)
            final[sentence] = column
        final.to_csv(f'./RawData/{person_folder}/person.csv', index=False)




def generate_group_csv():
    print('Generating an overview file of the persons\' categorical values.')
    persons = list()

    # Makes sure we scroll through all the relevant folders: starts with "Personne" and is actually a folder.
    for person_folder in [file for file in os.listdir('./RawData/') if os.path.isdir(f'./RawData/{file}')]:

        with open(f'./RawData/{person_folder}/etc/README', 'r') as input:
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
            'ID': person_folder,
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


def extract_data(person, sentence):
    print('Extracting the data from the CSV files.')

    raw_data = pd.read_csv(f'./RawData/{person}/wav/{sentence.removesuffix(".wav")}.csv')

    column_names = raw_data.columns
    data_to_use = raw_data.values

    x_data_temp = list()
    y_data_temp = list()

    print(person, sentence)
    for i in range(0, data_to_use.shape[0] - time_window_length, non_overlap_length):
        x = data_to_use[i: i + time_window_length]
        start_time = time.time()
        # Extract features
        feature_vector, features = extract_features(x)
        end_time = time.time()
        global total_time
        total_time = total_time + (end_time - start_time)


        x_data_temp.append(feature_vector)
        y_data_temp.append(sentence)
        
    return column_names, features, x_data_temp, y_data_temp


def generate_dataset():
    # Initialization
    persons = [person for person in os.listdir('./RawData/') if os.path.isdir(f'./RawData/{person}')]
    
    arguments = [tuple((person, sentence)) for person in persons for sentence in sentences]

    # for person, sentence in arguments:
    #     column_names, features = extract_data(person, sentence)

    with concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as e:
        futures = [e.submit(extract_data, person, sentence) for person, sentence in arguments]
        for future in concurrent.futures.as_completed(futures):
            column_names, features, x_data_temp, y_data_temp = future.result()
            global x_data
            x_data.append(x_data_temp)
            global y_data
            y_data.append(y_data_temp)

    new_column_names = list()

    for feature in features:
        for column_name in column_names:
            new_column_names.append(f'{feature}_{column_name}')


    x_data = pd.DataFrame(x_data, columns=new_column_names)
    # x_data.insert(0, 'Label', label_data)  # If we can to retrieve the file easily
    x_data.to_csv('x_data.csv', index=False)

    print(f'The total time to extract all features is: {total_time}.')
    print(f'The size of the dataset is: {x_data.shape[0]} by {x_data.shape[1]} (instances x features).')
    print(f'The number of labels is: {len(y_data)}.')

    # Save the dataset
    with open('dataset.pickle', 'wb') as output:
        pickle.dump([x_data, y_data], output)

if __name__ == '__main__':
    convert_to_csv()

    convert_to_csv_with_quarters()

    one_csv_per_person()

    generate_group_csv()

    clean_data()

    # generate_dataset()

    print('We are the champions 🎶')