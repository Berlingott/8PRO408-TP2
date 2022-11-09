import os
import pickle

import numpy as np

from sklearn.ensemble import ExtraTreesClassifier

from matplotlib import pyplot as plt

# USER PARAMETERS
path_name = "dataset.pickle"

attribute_number_to_select = 6


# LOAD THE DATASET
with open(path_name, "rb") as file:
    x, y = pickle.load(file)


# DIMENTIONALITY REDUCTION
classifier_model = ExtraTreesClassifier(n_estimators=50)

classifier_model = classifier_model.fit(x, y)

importance_score = classifier_model.feature_importances_

indices = np.argsort(importance_score)[::-1]

columns_to_select = x.columns[indices[0:attribute_number_to_select]]

new_dataset = x[columns_to_select]


# PLOT RESULTS
plt.bar(x=np.arange(attribute_number_to_select), height=importance_score[indices[0:attribute_number_to_select]],
        tick_label=columns_to_select)
plt.title("Feature Importance - Sum=" + str(np.sum(importance_score[indices[0:attribute_number_to_select]])))
plt.xlabel("Selected features")
plt.xticks(rotation=90)
plt.ylabel("Importance score")
plt.tight_layout()
plt.show()

# SAVE MY NEW DATASET
with open(os.path.join('selected_features.pickle'), "wb") as f:
    pickle.dump([new_dataset, y], f)





