from pydoc import plain

from matplotlib import
import pandas as pd


df = pd.read_csv("avgIQpercountry.csv")

avg_iq_by_continent = df,grupby("Continent")["Average IQ"].mean()


plt.figure(figsize=(10,6))

avg_iq_by_continent.plot(kind="line",marker="o", color="skyblue")

plt.show()