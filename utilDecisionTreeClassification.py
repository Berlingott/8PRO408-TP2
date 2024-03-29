########################################################################################################################
# Author : Julien Maitre                                                                                               #
# Date : 01 - 31 - 2019                                                                                                #
# Version : 0.1                                                                                                        #
########################################################################################################################

""" This file defines the functions for a decision tree classifier.
    It allows to train, test (even cross validate), compute the performances and display the results. """

import time

import numpy as np
import itertools
import matplotlib.pyplot as plt

from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import accuracy_score, cohen_kappa_score, confusion_matrix, classification_report,\
    matthews_corrcoef, hamming_loss, precision_score, recall_score, f1_score

import pandas as pd
import pickle
import plotly.express as px
import plotly.graph_objects as go

########################################################################################################################
#                            Define the Classes to be Used for the Decision Tree Classifier                            #
########################################################################################################################


class DecisionTreeParameters(object):

    def __init__(self, criterion='gini', max_depth=None, min_samples_split=2, min_samples_leaf=1,
                 min_weight_fraction_leaf=0., max_features="sqrt", max_leaf_nodes=None):

        self.criterion = criterion
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.min_weight_fraction_leaf = min_weight_fraction_leaf
        self.max_features = max_features
        self.max_leaf_nodes = max_leaf_nodes


########################################################################################################################
#                  Define the Classes to be Used for the Performances of the Decision Tree Classifier                  #
########################################################################################################################


class PerformancesDecisionTree(object):

    def __init__(self, accuracy_fraction=None, accuracy_number=None, cohen_kappa_score=None,
                 confusion_matrix_without_normalization=None, confusion_matrix_with_normalization=None,
                 classification_report=None, hamming_loss=None, jaccard_similarity_score_with_normalization=None,
                 jaccard_similarity_score_without_normalization=None, micro_precision=None, macro_precision=None,
                 weighted_precision=None, none_precision=None, micro_recall=None, macro_recall=None,
                 weighted_recall=None, none_recall=None, micro_f1_score=None, macro_f1_score=None,
                 weighted_f1_score=None, none_f1_score=None, matthews_corrcoef=None):

        self.accuracy_score_fraction = accuracy_fraction
        self.accuracy_score_number = accuracy_number

        self.cohen_kappa_score = cohen_kappa_score

        self.confusion_matrix_without_normalization = confusion_matrix_without_normalization
        self.confusion_matrix_with_normalization = confusion_matrix_with_normalization

        self.classification_report = classification_report

        self.hamming_loss = hamming_loss

        self.micro_precision = micro_precision
        self.macro_precision = macro_precision
        self.weighted_precision = weighted_precision
        self.none_precision = none_precision

        self.micro_recall = micro_recall
        self.macro_recall = macro_recall
        self.weighted_recall = weighted_recall
        self.none_recall = none_recall

        self.micro_f1_score = micro_f1_score
        self.macro_f1_score = macro_f1_score
        self.weighted_f1_score = weighted_f1_score
        self.none_f1_score = none_f1_score

        self.matthews_corrcoef = matthews_corrcoef


########################################################################################################################
#                         Define the Functions for the Training of the Decision Tree Classifier                        #
########################################################################################################################


def train_decision_tree_classifier(x_train, y_train, decision_tree_parameters):

    # Print information in the console
    print("\nThe decision tree classifier will be created")

    criterion = decision_tree_parameters.criterion
    max_depth = decision_tree_parameters.max_depth
    min_samples_split = decision_tree_parameters.min_samples_split
    min_samples_leaf = decision_tree_parameters.min_samples_leaf
    min_weight_fraction_leaf = decision_tree_parameters.min_weight_fraction_leaf
    max_features = decision_tree_parameters.max_features
    max_leaf_nodes = decision_tree_parameters.max_leaf_nodes

    # Create an instance of the decision tree classifier
    decision_tree_classifier = DecisionTreeClassifier(criterion=criterion,
                                                      max_depth=max_depth,
                                                      min_samples_split=min_samples_split,
                                                      min_samples_leaf=min_samples_leaf,
                                                      min_weight_fraction_leaf=min_weight_fraction_leaf,
                                                      max_features=max_features,
                                                      max_leaf_nodes=max_leaf_nodes)

    # Print information in the console
    print("The decision tree classifier has been created")
    print("The decision tree classifier is training")

    # Get the start time of the training process
    start_time = time.time()

    # Train the model using the training sets
    decision_tree_classifier.fit(x_train, y_train)

    # Get the end time of the training process
    end_time = time.time()

    # Compute the time that the training process took
    running_time = end_time - start_time

    # Print information in the console
    print("The decision tree classifier has done its training process")

    return decision_tree_classifier, running_time


########################################################################################################################
#                      Define the Functions for the Testing of the Decision Tree Classifier                      #
########################################################################################################################


def test_decision_tree_classifier(x_test, decision_tree_classifier):

    # Print information in the console
    print("\nThe decision tree classifier is being tested with the testing set")

    # Get the start time of the testing process
    start_time = time.time()

    # Make predictions using the testing set
    y_test_predicted = decision_tree_classifier.predict(x_test)

    # Get the end time of the testing process
    end_time = time.time()

    # Compute the time that the testing process took
    running_time = end_time - start_time

    # Print information in the console
    print("The decision tree classifier has done its testing process")

    return y_test_predicted, running_time


########################################################################################################################
#                    Define the Functions for Computing Performances of the Decision Tree Classifier                   #
########################################################################################################################


def compute_performances_for_multiclass(y_test, y_test_predicted, class_names, performances):

    # Compute the accuracy classification score : return the fraction of correctly classified samples
    performances.accuracy_score_fraction = accuracy_score(y_test, y_test_predicted, normalize=True)
    # Compute the accuracy classification score : return return the number of correctly classified samples
    performances.accuracy_score_number = accuracy_score(y_test, y_test_predicted, normalize=False)

    # Print information in the console
    print("\nAccuracy classification score : ")
    print("         Fraction of correctly classified samples : %.2f" % performances.accuracy_score_fraction)
    print("         Number of correctly classified samples: %.2f" % performances.accuracy_score_number)

    # Compute the Cohen's kappa score
    performances.cohen_kappa_score = cohen_kappa_score(y_test, y_test_predicted)

    # Print information in the console
    print("\nCohen's kappa score : %.2f" % performances.cohen_kappa_score)

    # Compute the confusion matrix without normalization
    performances.confusion_matrix_without_normalization = confusion_matrix(y_test, y_test_predicted)
    # Compute the confusion matrix with normalization
    performances.confusion_matrix_with_normalization = \
        performances.confusion_matrix_without_normalization.astype('float') \
        / performances.confusion_matrix_without_normalization.sum(axis=1)[:, np.newaxis]

    # Print information in the console
    print("\nConfusion matrix : ")
    print("     Confusion matrix without normalization : ")
    square_matrix_size = len(performances.confusion_matrix_without_normalization)
    for i in range(square_matrix_size):
        if i == 0:
            print('                 [' + np.array2string(performances.confusion_matrix_without_normalization[i]))
        elif i == square_matrix_size -1:
            print('                  ' + np.array2string(performances.confusion_matrix_without_normalization[i]) + ']')
        else:
            print('                  ' + np.array2string(performances.confusion_matrix_without_normalization[i]))
    print("     Confusion matrix with normalization : ")
    square_matrix_size = len(performances.confusion_matrix_with_normalization)
    for i in range(square_matrix_size):
        if i == 0:
            print('                 [' + np.array2string(performances.confusion_matrix_with_normalization[i]))
        elif i == square_matrix_size - 1:
            print('                  ' + np.array2string(performances.confusion_matrix_with_normalization[i]) + ']')
        else:
            print('                  ' + np.array2string(performances.confusion_matrix_with_normalization[i]))

    # Compute the classification_report
    performances.classification_report = classification_report(y_test, y_test_predicted, target_names=class_names,
                                                               digits=4)

    # Print information in the console
    print("\nclassification_report : ")
    print(performances.classification_report)

    # Compute the average Hamming loss
    performances.hamming_loss = hamming_loss(y_test, y_test_predicted)

    # Print information in the console
    print("\nAverage Hamming loss : %.2f" % performances.hamming_loss)

    # Compute the precision
    performances.micro_precision = precision_score(y_test, y_test_predicted, average='micro')
    performances.macro_precision = precision_score(y_test, y_test_predicted, average='macro')
    performances.weighted_precision = precision_score(y_test, y_test_predicted, average='weighted')
    performances.none_precision = precision_score(y_test, y_test_predicted, average=None)

    # Print information in the console
    print("\nPrecision score : ")
    print("     micro : %.2f" % performances.micro_precision)
    print("     macro : %.2f" % performances.macro_precision)
    print("     weighted : %.2f" % performances.weighted_precision)
    print("     None : " + np.array2string(performances.none_precision))
    print("     Classes : " + np.array2string(class_names))

    # Compute the recall
    performances.micro_recall = recall_score(y_test, y_test_predicted, average='micro')
    performances.macro_recall = recall_score(y_test, y_test_predicted, average='macro')
    performances.weighted_recall = recall_score(y_test, y_test_predicted, average='weighted')
    performances.none_recall = recall_score(y_test, y_test_predicted, average=None)

    # Print information in the console
    print("\nRecall score : ")
    print("     micro : %.2f" % performances.micro_recall)
    print("     macro : %.2f" % performances.macro_recall)
    print("     weighted : %.2f" % performances.weighted_recall)
    print("     None : " + np.array2string(performances.none_recall))
    print("     Classes : " + np.array2string(class_names))

    # Compute the F1 score
    performances.micro_f1_score = f1_score(y_test, y_test_predicted, average='micro')
    performances.macro_f1_score = f1_score(y_test, y_test_predicted, average='macro')
    performances.weighted_f1_score = f1_score(y_test, y_test_predicted, average='weighted')
    performances.none_f1_score = f1_score(y_test, y_test_predicted, average=None)

    # Print information in the console
    print("\nF1-score : ")
    print("     micro : %.2f" % performances.micro_f1_score)
    print("     macro : %.2f" % performances.macro_f1_score)
    print("     weighted : %.2f" % performances.weighted_f1_score)
    print("     None : " + np.array2string(performances.none_f1_score))
    print("     Classes : " + np.array2string(class_names))

    # Compute the Matthews correlation coefficient
    performances.matthews_corrcoef = matthews_corrcoef(y_test, y_test_predicted)

    # Print information in the console
    print("\nMatthews correlation coefficient : %.2f" % performances.matthews_corrcoef)

    return performances


########################################################################################################################
#              Define the Functions to Display the Results on Graph for the Decision Tree Classifier             #
########################################################################################################################

def plotly_confusion_matrix(performances, class_names, title='Confusion matrix', cmap=plt.cm.Blues):

    cm = performances.confusion_matrix_without_normalization

    fig = px.imshow(cm,
                    x=class_names,
                    y=class_names,
                    text_auto=True,
                    title=title,
                    labels=dict(x ="Predicted label",
                                y ="True label")
                    )
    fig.write_image(f"Graphs/confusion_matrix.png")


def plotly_features_and_classification_for_dt_classifier(x, y, class_names, decision_tree_classifier,
                                                         decision_tree_parameters):

    number_of_classes = len(class_names)
    number_of_features = len(x[0])

    all_combination = list(itertools.combinations(range(number_of_features), 2))
    number_of_combination = len(all_combination)

    # Step size in the mesh
    h = .01

    for i in range(number_of_combination):

        indice_1 = all_combination[i][0]
        indice_2 = all_combination[i][1]

        colors = [class_names[item] for item in y]
        with open("selected_features.pickle", "rb") as file:
            columns = pickle.load(file)
        columns = pd.DataFrame(columns[0])
        columns = columns.columns

        fig = px.scatter(x = x[:, indice_1],
                            y = x[:, indice_2],
                            color=colors,
                            title=f'{number_of_classes}-Class Classification',
                            labels=dict(x = columns[indice_1],
                                        y = columns[indice_2]),
                            color_discrete_sequence=px.colors.qualitative.G10)

        if ((number_of_combination % 2) == 1) and (number_of_combination <= 1):

            # Plot the decision boundary.
            # For that, we will assign a color to each point in the mesh [x_min, x_max]x[y_min, y_max].
            x_min, x_max = x[:, indice_1].min() - 1, x[:, indice_1].max() + 1
            y_min, y_max = x[:, indice_2].min() - 1, x[:, indice_2].max() + 1

            xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

            fig.update_xaxes(range=[xx.min(), xx.max()])
            fig.update_yaxes(range=[yy.min(), yy.max()])
            
        fig.write_image(f'Graphs/{indice_1}{indice_2}.png')