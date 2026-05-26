import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("asvgIQpercountry.csv")

filtred_df = df[df["Avarage IQ"]>=100]

filtred_df = filtred_df.sort_values(by="Avarage IQ", ascending=False)


print(filtred_df)

plt.figure(figsize=(14,8))

bars = plt.bar(filtred_df["Country"],filtred_df["Avarage IQ"], color ="skyblue")


plt.title("Average IQ by Country(IQ>100)",fontsize=16)

plt.xlabel("Country",fontsize=14)
plt.xlabel("Avarage IQ",fontsize=14)

plt.xtivks(rotation=90,fontsize=10)
plt.ytivks(fontsize=10)

plt.grid(axis=  "y",linestyle ="--",alpha = 0.8)

plt.bar_label(bars,fmt="%.2f",fontsize=10,color="black")

plt.tight_layout()

plt.show()