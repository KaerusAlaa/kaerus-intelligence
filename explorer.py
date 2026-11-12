import pandas as pd

tableau = pd.read_excel("data/ema_medicines_2026-11-12.xlsx", skiprows=8)

print(tableau.shape)
print(tableau["Category"].value_counts())
print(tableau["Medicine status"].value_counts())
