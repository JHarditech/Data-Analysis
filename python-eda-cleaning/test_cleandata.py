import csv 
import pandas as pd
import numpy as np 

# Load the CSV file
df = pd.read_csv('winemag-data-130k-v2.csv')

# Basic cleaning: drop rows with missing values
df_clean = df.dropna()

# Summarise key statistics
summary = df_clean.describe(include='all')

# Save cleaned data and summary
df_clean.to_csv('data_cleaned.csv', index=False)
summary.to_csv('data_summary.csv')

print("Cleaned data and summary statistics have been saved.")