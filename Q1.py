import pandas as pd
import numpy as np


def read_dataset(file_name):
    """
    This function loads data from csv file
    :param file_name: the name of csv file
    :return: training set data and y star matrix
    """
    data = pd.read_csv(file_name)
    dataset_train_values = data.iloc[:, 0:data.shape[1] - 1].values
    y_star = data.iloc[:, data.shape[1] - 1:data.shape[1]].values
    y_star = y_star.reshape(len(y_star), 1)
    return dataset_train_values, y_star


def calculate_weight_vector(X, Y):
    x_new = np.array(X)
    x_new_transpose = x_new.transpose()
    temp = np.dot(x_new_transpose, x_new)
    temp = temp + 0.001 * np.identity(x_new_transpose.shape[0], dtype=float)
    temp = np.linalg.inv(temp)
    temp = np.dot(temp, x_new_transpose)
    temp = np.dot(temp, Y)
    return temp


def run():
    training_set, y_star = read_dataset('diabetes.csv')
    weight_vector = calculate_weight_vector(training_set, y_star)
