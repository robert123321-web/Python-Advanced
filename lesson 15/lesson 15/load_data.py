import pandas as pd

# Load dataset
df = pd.read_csv("weather_tokyo_data.csv")

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Extract month
df['month'] = df['date'].dt.month