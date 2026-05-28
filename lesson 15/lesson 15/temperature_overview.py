from load_data import df

# Average temperature for entire dataset
overall_avg_temp = df['temperature'].mean()

print("Average Temperature (Entire Dataset):")
print(f"{overall_avg_temp:.2f} °C")