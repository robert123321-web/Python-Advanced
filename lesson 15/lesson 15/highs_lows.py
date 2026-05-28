from load_data import df

# Hottest day
hottest_day = df.loc[df['temperature'].idxmax()]

# Coldest day
coldest_day = df.loc[df['temperature'].idxmin()]

print("Hottest Day:")
print(hottest_day)

print("\nColdest Day:")
print(coldest_day)