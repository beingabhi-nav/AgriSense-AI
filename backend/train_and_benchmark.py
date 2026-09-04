import time
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from ml_core.random_forest_classifier import CustomRandomForestClassifier

def load_real_data(csv_path="crop_recommendation.csv"):
    df = pd.read_csv(csv_path)
    X = df.drop("label", axis=1).values
    y = df["label"].values
    return train_test_split(X, y, test_size=0.2, random_state=42)

def run_benchmark():
    print("--- Starting Crop Recommendation Benchmark ---")
    
    # 1. Load the real Kaggle data
    print("Loading real dataset...")
    X_train, X_test, y_train, y_test = load_real_data()

    # 2. Train and evaluate Custom Model
    print("Training Custom Random Forest...")
    start_time = time.time()
    custom_rf = CustomRandomForestClassifier(n_trees=10, max_depth=10)
    custom_rf.fit(X_train, y_train)
    custom_preds = custom_rf.predict(X_test)
    custom_time = time.time() - start_time
    custom_acc = accuracy_score(y_test, custom_preds)

    # 3. Train and evaluate Scikit-Learn Model
    print("Training Scikit-Learn Random Forest...")
    start_time = time.time()
    sklearn_rf = RandomForestClassifier(n_estimators=5, max_depth=5, random_state=42)
    sklearn_rf.fit(X_train, y_train)
    sklearn_preds = sklearn_rf.predict(X_test)
    sklearn_time = time.time() - start_time
    sklearn_acc = accuracy_score(y_test, sklearn_preds)

    # 4. Print Results
    print("\n--- Benchmark Results ---")
    print("Custom Model   | Accuracy: {:.2f} | Time: {:.4f} sec".format(custom_acc, custom_time))
    print("Sklearn Model  | Accuracy: {:.2f} | Time: {:.4f} sec".format(sklearn_acc, sklearn_time))
        
    # Save the high-accuracy custom model
    joblib.dump(custom_rf, "custom_random_forest.pkl")
    print("Custom model saved successfully as custom_random_forest.pkl")

if __name__ == "__main__":
    run_benchmark()