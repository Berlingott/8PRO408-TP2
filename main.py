import os

import pandas as pd

import time

from featureExtraction import extract_features
import pickle

# USER PARAMETERS

raw_dataset_pathname = "./CleanData"

object_list = [person for person in os.listdir('./RawData/')]

# Using a window length that is too short causes sets of values
# that are too similar. This in turn generates NaNs for kurtosis
# and skewness. The dimentionality reduction tool does not support
# NaNs. For that reason a wider window needs to be applied.
time_window_length = 500
overlap_length = 250

extracted_dataset_pathname = "."

new_dataset_name = "new_dataset"


# INITIALIZATION

folder_list = os.listdir(raw_dataset_pathname)
folder_number = len(folder_list)

non_overlap_length = time_window_length - overlap_length


# CREATE THE DATASET

x_data = []
y_data = []

total_time = 0

for folder_name in folder_list:

    print("We are processing: " + folder_name)

    tmp_pathname = os.path.join(raw_dataset_pathname, folder_name)

    file_list = os.listdir(tmp_pathname)

    for file_name in file_list:

        for object in object_list:

            if object in file_name:

                print("     - " + file_name)

                raw_data = pd.read_csv(os.path.join(tmp_pathname, file_name),
                                       sep=",", skiprows=0, engine="python")

                column_names = raw_data.columns

                data_to_use = raw_data.values

                for k in range(0, data_to_use.shape[0] - time_window_length, non_overlap_length):

                    x = data_to_use[k: k+time_window_length]

                    start_time = time.time()
                    # Extract features
                    vector_features, feature_list = extract_features(x)
                    end_time = time.time()


                    total_time = total_time + (end_time - start_time)

                    x_data.append(vector_features)
                    y_data.append(object)

new_column_names = []

for feature in feature_list:

    for column_name in column_names:

        new_column_names.append(feature + "_" + column_name)

x_data = pd.DataFrame(x_data, columns=new_column_names)

print("\n\nThe total time to extract all features is: " + str(total_time))

print("The size of the dataset is: " + str(x_data.shape[0]) + "x" + str(x_data.shape[1]) + "(instances x features)")
print("The number of labels is: " + str(len(y_data)))

# SAVE THE DATASET
with open(os.path.join(extracted_dataset_pathname, new_dataset_name + ".pickle"), "wb") as f:
    pickle.dump([x_data, y_data], f)







