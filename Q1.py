import pandas as pd
import numpy as np
import math


def read_dataset(file_name):
    """
    This function loads data from csv file
    :param file_name: the name of csv file
    :return: training set data and y_star matrix
    """
    data = pd.read_csv(file_name)
    dataset_train_values = data.iloc[:, 0:data.shape[1] - 1].values
    y_star = data.iloc[:, data.shape[1] - 1:data.shape[1]].values
    y_star = y_star.reshape(len(y_star), 1)
    return dataset_train_values, y_star


def calculate_weight_vector(X, Y):
    """
    This function will calculate the exact value of weight vector matrix
    :param X: training set
    :param Y: out puts
    :return: weight vector
    """
    x_new = np.array(X)
    x_new_transpose = x_new.transpose()
    temp = np.dot(x_new_transpose, x_new)
    temp = temp + 0.001 * np.identity(x_new_transpose.shape[0], dtype=float)
    temp = np.linalg.inv(temp)
    temp = np.dot(temp, x_new_transpose)
    temp = np.dot(temp, Y)
    return temp


def calculate_y_out(training_set, weight_vector):
    """
    This function will calculate y based on given x and w
    :param training_set: is x
    :param weight_vector: is w
    :return: y
    """
    return np.dot(training_set, weight_vector)


def evaluate_model(y_out, y_star):
    """
    This function will calculate sum of squared error
    :param y_out: what the model predicted
    :param y_star: the actual value
    :return: error value
    """
    error = 0
    number_of_correct_predicted = 0
    for index, i in enumerate(y_out):
        error += math.pow((y_out[index] - y_star[index]), 2)
        if y_out[index] >= 0.5:
            z = 1
        else:
            z = 0
        if z == y_star[index]:
            number_of_correct_predicted += 1
    error = math.sqrt(error)
    return error, number_of_correct_predicted


def run():
    training_set, y_star = read_dataset('diabetes.csv')
    weight_vector = calculate_weight_vector(training_set, y_star)
    y_out = calculate_y_out(training_set, weight_vector)
    error, correct_predicted = evaluate_model(y_out, y_star)
    print("Sum of Squared Error: " + str(error))
    print("Number of Correct Prediction: " + str(correct_predicted))
    print("Accuracy: " + str((correct_predicted / len(y_out)) * 100) + "%")
