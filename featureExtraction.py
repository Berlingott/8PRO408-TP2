import numpy as np
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

def extract_features(data):

    tmp = extract_min(data)
    tmp = np.append(tmp, extract_max(data))
    tmp = np.append(tmp, extract_mean(data))
    tmp = np.append(tmp, extract_std(data))
    tmp = np.append(tmp, extract_skewness(data))
    tmp = np.append(tmp, extract_kurtosis(data))

    return tmp, ["min", "max", "mean", "std", "skew", "kurt"]