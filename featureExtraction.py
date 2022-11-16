import numpy as np
import pandas as pd
from scipy import stats


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

    return tmp, ["min", "max", "mean", "std", "skew", "kurt", "diff", "sum", "slope", "count"]