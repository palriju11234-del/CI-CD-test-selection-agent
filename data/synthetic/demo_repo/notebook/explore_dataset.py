import pandas as pd

# Load the dataset
df = pd.read_csv("data/claims.csv")

# Display the first 5 rows
print("First 5 rows:")
print(df.head())

print("\n----------------------")

# Display column names
print("Columns:")
print(df.columns)

print("\n----------------------")

# Dataset shape
print("Dataset Shape:")
print(df.shape)

print("\n----------------------")

# Check for missing values
print("Missing Values:")
print(df.isnull().sum())

print("\n----------------------")

# Count each label
print("Label Distribution:")
print(df["label"].value_counts())