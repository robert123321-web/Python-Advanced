from load_data import df
import matplotlib.pyplot as plt

# Function to determine season
def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Autumn'

# Create season column
df['season'] = df['month'].apply(get_season)

# Seasonal averages
seasonal_avg_temp = df.groupby('season')['temperature'].mean()

print("Seasonal Average Temperature:")
print(seasonal_avg_temp)

# Bar Plot
plt.figure(figsize=(8, 5))
seasonal_avg_temp.plot(kind='bar')

plt.title("Seasonal Average Temperature")
plt.xlabel("Season")
plt.ylabel("Average Temperature (°C)")
plt.xticks(rotation=0)

plt.show()