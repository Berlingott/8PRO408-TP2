import numpy as np
import matplotlib.pyplot as plt

import utilDecisionTreeClassification
from sklearn import datasets
from sklearn.model_selection import train_test_split

import pickle

########################################################################################################################
#                                    User Settings for the Decision Tree Classifier                                    #
########################################################################################################################

# Define the path of the dataset
with open("selected_features.pickle", "rb") as file:
    dataset = pickle.load(file)

# Create a class object that define parameters of the decision tree classifier
decision_tree_parameters = utilDecisionTreeClassification.DecisionTreeParameters()

""" Function to measure the quality of a split
    Supported criteria are “gini” for the Gini impurity and “entropy” for the information gain. 
    Note: this parameter is tree-specific. """
decision_tree_parameters.criterion = 'entropy'

""" The strategy used to choose the split at each node. 
    Supported strategies are “best” to choose the best split and “random” to choose the best random split."""
decision_tree_parameters.splitter = 'best'

""" The maximum depth of the tree.
    The choices are :
                    If None, then nodes are expanded until all leaves are pure or until all leaves contain less than 
                        min_samples_split samples. """
decision_tree_parameters.max_depth = None

""" The minimum number of samples required to split an internal node :
    The choices are :
                      If int, then consider min_samples_leaf as the minimum number.
                      If float, then min_samples_leaf is a fraction and ceil(min_samples_leaf * n_samples) are 
                        the minimum number of samples for each node."""
decision_tree_parameters.min_samples_split = 2

""" The minimum number of samples required to be at a leaf node.
    The choices are :
                      If int, then consider min_samples_split as the minimum number.
                      If float, then min_samples_split is a fraction and ceil(min_samples_split * n_samples) are the 
                        minimum number of samples for each split. """
decision_tree_parameters.min_samples_leaf = 1

""" The number of features to consider when looking for the best split
    The choices are :
                      If int, then consider max_features features at each split.
                      If float, then max_features is a fraction and int(max_features * n_features) features are considered at each split.
                      If “auto”, then max_features=sqrt(n_features).
                      If “sqrt”, then max_features=sqrt(n_features) (same as “auto”).
                      If “log2”, then max_features=log2(n_features).
                      If None, then max_features=n_features. 

    Note: the search for a split does not stop until at least one valid partition of the node samples is found, even 
    if it requires to effectively inspect more than max_features features."""
decision_tree_parameters.max_feature = 'sqrt'

""" Grow trees with max_leaf_nodes in best-first fashion. 
    If None then unlimited number of leaf nodes. """
decision_tree_parameters.max_leaf_nodes = None

########################################################################################################################
#                                  Display Information, Convert and Create Variables                                   #
########################################################################################################################

class_names = sorted(list(set(dataset[1])))

X = np.array(dataset[0])
y = [class_names.index(person) for person in dataset[1]]

# Get the training and testing datasets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

print("     The training dataset has : " + str(len(X_train)) + " instances\n")
print("     The testing dataset has : " + str(len(X_test)) + " instances\n")
print("     All the instances are splitting into " + str(len(class_names)) + " classes, which are : \n")

for i in range(0, len(class_names), 1):
    print("         - " + class_names[i] + "\n")

# Convert the list of class names into an array to display results
class_names = np.array(class_names)  # It was useful in a previous version of this code

# Create a class object that define the performances container of the decision tree classifier
performances = utilDecisionTreeClassification.PerformancesDecisionTree()

########################################################################################################################
#                                  Execute the Decision Tree Classifier on the Dataset                                 #
########################################################################################################################

print("The decision tree algorithm is executing. Please wait ...")

# Create and train the decision tree classifier
decision_tree_classifier, training_running_time = \
    utilDecisionTreeClassification.train_decision_tree_classifier(X_train, y_train, decision_tree_parameters)

# Print information in the console
print("The training process of decision tree classifier took : %.8f second" % training_running_time)

# Test the decision tree classifier
y_test_predicted, testing_running_time = \
    utilDecisionTreeClassification.test_decision_tree_classifier(X_test, decision_tree_classifier)

# Print information in the console
print("The testing process of decision tree classifier took : %.8f second" % testing_running_time)

# Compute the performances of the decision tree classifier
cm = utilDecisionTreeClassification.compute_performances_for_multiclass(y_test, y_test_predicted, class_names,
                                                                        performances)

# Display the results
utilDecisionTreeClassification.display_confusion_matrix(performances, class_names)
utilDecisionTreeClassification.display_features_and_classification_for_dt_classifier(X_test, y_test, class_names,
                                                                                     decision_tree_classifier,
                                                                                     decision_tree_parameters)

plt.show()