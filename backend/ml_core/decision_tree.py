import numpy as np
from collections import Counter

class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, *, value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value

    def is_leaf_node(self):
        return self.value is not None

class DecisionTree:
    def __init__(self, min_samples_split=2, max_depth=100, task='classification'):
        self.min_samples_split = min_samples_split
        self.max_depth = max_depth
        self.task = task
        self.root = None

    def fit(self, X, y):
        # Placeholder for the recursive tree building logic
        # You will calculate Gini impurity or Variance reduction here
        pass

    def predict(self, X):
        # Placeholder for tree traversal
        return np.array([])