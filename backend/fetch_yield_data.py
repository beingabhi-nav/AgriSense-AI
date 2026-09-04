import kagglehub
import shutil
import os
import glob

print("Fetching Yield Prediction dataset from Kaggle...")
# Download latest version
path = kagglehub.dataset_download("patelris/crop-yield-prediction-dataset")

# Find the CSV in the cached folder and move it to the backend
csv_files = glob.glob(os.path.join(path, "*.csv"))
if csv_files:
    destination = "crop_yield.csv"
    shutil.copy(csv_files[0], destination)
    print(f"Success! Dataset moved to: {os.path.abspath(destination)}")
else:
    print("Error: No CSV file found in the downloaded dataset.")