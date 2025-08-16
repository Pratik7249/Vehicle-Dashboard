import pandas as pd
import numpy as np

np.random.seed(42)

months = pd.date_range(start="2023-01-01", end="2024-12-01", freq="MS")

categories = {
    "2W": ["Hero", "Bajaj", "TVS"],
    "3W": ["Piaggio", "Bajaj Auto"],
    "4W": ["Tata", "Hyundai", "Maruti"]
}

rows = []
for cat, mans in categories.items():
    for man in mans:
        base = np.random.randint(5000, 20000)
        growth = np.random.uniform(0.01, 0.05)
        val = base
        for m in months:
            val = val * (1 + growth + np.random.uniform(-0.02, 0.02))
            rows.append([m, cat, man, int(val)])

df = pd.DataFrame(rows, columns=["Date", "Category", "Manufacturer", "Registrations"])
df["YoY Growth %"] = df.groupby(["Category","Manufacturer"])["Registrations"].pct_change(periods=12) * 100
df["QoQ Growth %"] = df.groupby(["Category","Manufacturer"])["Registrations"].pct_change(periods=3) * 100

df.to_csv("registrations.csv", index=False)
print("✅ Mock dataset saved → registrations.csv")
