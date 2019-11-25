import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# For splitting the data into training and testing sets
from sklearn.model_selection import train_test_split
# For creating a decision tree and a visualization of the tree
from sklearn.tree import DecisionTreeClassifier, export_graphviz, plot_tree
# For analyzing the decision tree's performance
from sklearn.metrics import classification_report, confusion_matrix

"""
PART 1: Generates a decision tree and a visualization of it
"""

dataset = pd.read_csv("P4Data.csv")

x = dataset.drop("Class", axis=1)
y = dataset["Class"]

# To regenerate the figures in the document, add random_state=1599 to the
# arguments of the train_test_split function
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=.3)

plt.figure(dpi=200)

classifier = DecisionTreeClassifier()
classifier.fit(x_train, y_train)
plot_tree(classifier)

"""
PART 2: uses the decision tree to predict and display performance statistics
and confusion matrix
"""

y_pred = classifier.predict(x_test)

print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

"""
PART 3: creates a graph of the data and colors based on the way it was
classified by the decision tree
"""

plt.figure(figsize=(5,5))

# Colors regions of the graph based on the decision tree
h = 0.02
x_min, x_max = dataset['X'].min() - 10*h, dataset['X'].max() + 10*h
y_min, y_max = dataset['Y'].min() - 10*h, dataset['Y'].max() + 10*h
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))
Z = classifier.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)
plt.contourf(xx, yy, Z, cmap='Paired_r')

# Draws black borders around regions
plt.contour(xx, yy, Z, colors='k', linewidths=0.7)

# Plots the data with colors based on their actual class
y_all_pred = classifier.predict(x)
plt.scatter(dataset['X'], dataset['Y'], c=y_all_pred, cmap='Paired_r', edgecolors='k');
plt.show()
