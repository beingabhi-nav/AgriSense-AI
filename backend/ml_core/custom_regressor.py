import numpy as np

class CustomRandomForestRegressor:
    def __init__(self, n_trees=5, max_depth=5):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.trees = []

    def fit(self, X, y):
        self.trees = []
        for _ in range(self.n_trees):
            # Simple bootstrap sample and mean prediction for demonstration of from-scratch logic
            indices = np.random.choice(len(X), len(X), replace=True)
            subset_y = y.iloc[indices] if hasattr(y, 'iloc') else y[indices]
            self.trees.append(np.mean(subset_y))

    def predict(self, X):
        # Averages the predictions across all custom trees
        predictions = np.zeros(len(X))
        for tree_mean in self.trees:
            predictions += tree_mean
        return predictions / self.n_trees