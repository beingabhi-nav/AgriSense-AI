import pandas as pd
import time
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib
from ml_core.custom_regressor import CustomRandomForestRegressor

def train_yield():
    print("Loading crop yield dataset...")
    df = pd.read_csv("crop_yield.csv")
    
    # Drop rows with missing values to fix the NaN error
    df = df.dropna()
    
    numeric_df = df.select_dtypes(include=['number'])
    
    y = numeric_df.iloc[:, -1]
    X = numeric_df.iloc[:, :-1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training Custom Regressor (From Scratch)...")
    start = time.time()
    custom_model = CustomRandomForestRegressor(n_trees=10)
    custom_model.fit(X_train, y_train)
    custom_preds = custom_model.predict(X_test)
    print(f"Custom MAE: {mean_absolute_error(y_test, custom_preds):.2f} | Time: {time.time()-start:.4f}s")

    print("Training Scikit-Learn Regressor...")
    start = time.time()
    sk_model = RandomForestRegressor(n_estimators=10, random_state=42)
    sk_model.fit(X_train, y_train)
    sk_preds = sk_model.predict(X_test)
    print(f"Sklearn MAE: {mean_absolute_error(y_test, sk_preds):.2f} | Time: {time.time()-start:.4f}s")
    
    joblib.dump(custom_model, "custom_yield_model.pkl")
    print("Yield regression model saved successfully as custom_yield_model.pkl")

if __name__ == "__main__":
    train_yield()