from load_data import df
import matplotlib.pyplot as plt

# Line graph
plt.figure(figsize=(12, 5))

plt.plot(df['date'], df['temperature'])

plt.title("Temperature Trend Over Time")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")

plt.show()