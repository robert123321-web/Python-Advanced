from load_data import df
import matplotlib.pyplot as plt

# Average temperature per month
monthly_avg_temp = df.groupby('month')['temperature'].mean()

print("Monthly Average Temperature:")
print(monthly_avg_temp)

# Bar Plot
plt.figure(figsize=(10, 5))
monthly_avg_temp.plot(kind='bar')

plt.title("Monthly Average Temperature")
plt.xlabel("Month")
plt.ylabel("Average Temperature (°C)")
plt.xticks(rotation=0)

plt.show()