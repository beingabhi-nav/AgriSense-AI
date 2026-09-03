import numpy as np
import time
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from ml_core.random_forest_classifier import CustomRandomForestClassifier

def generate_mock_agri_data(num_samples=500):
    # Simulating N, P, K, temperature, humidity, pH, rainfall
    np.random.seed(42)
    X = np.random.rand(num_samples, 7) * 100 
    # Simulating 3 crop classes (0, 1, 2)
    y = np.random.randint(0, 3, num_samples)
    return X, y

def run_benchmark():
    print("--- Starting Crop Recommendation Benchmark ---")
    X, y = generate_mock_agri_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 1. Train and evaluate Custom Model
    print("Training Custom Random Forest...")
    start_time = time.time()
    custom_rf = CustomRandomForestClassifier(n_trees=5, max_depth=5)
    custom_rf.fit(X_train, y_train)
    custom_preds = custom_rf.predict(X_test)
    custom_time = time.time() - start_time
    custom_acc = accuracy_score(y_test, custom_preds)

    # 2. Train and evaluate Scikit-Learn Model
    print("Training Scikit-Learn Random Forest...")
    start_time = time.time()
    sklearn_rf = RandomForestClassifier(n_estimators=5, max_depth=5, random_state=42)
    sklearn_rf.fit(X_train, y_train)
    sklearn_preds = sklearn_rf.predict(X_test)
    sklearn_time = time.time() - start_time
    sklearn_acc = accuracy_score(y_test, sklearn_preds)

    # 3. Print Results
    print("\n--- Benchmark Results ---")
    print("Custom Model   | Accuracy: {:.2f} | Time: {:.4f} sec".format(custom_acc, custom_time))
    print("Sklearn Model  | Accuracy: {:.2f} | Time: {:.4f} sec".format(sklearn_acc, sklearn_time))
    
if __name__ == "__main__":
    run_benchmark()