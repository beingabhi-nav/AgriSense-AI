import kagglehub
import shutil
import os

print("Fetching official dataset from Kaggle...")
# Download latest version to Kaggle's cache
cache_path = kagglehub.dataset_download("atharvaingle/crop-recommendation-dataset")

# The exact file name inside the Kaggle dataset
source_file = os.path.join(cache_path, "Crop_recommendation.csv")
destination = "crop_recommendation.csv"

# Copy it into your backend folder
shutil.copy(source_file, destination)
print(f"Success! Dataset moved to: {os.path.abspath(destination)}")