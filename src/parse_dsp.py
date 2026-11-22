import pandas as pd
import os

files = os.listdir("data/raw/dsp")
tables = []

for file_name in files:
    if file_name.startswith("~$"):
        continue
    df = pd.read_excel(f"data/raw/dsp/{file_name}", sheet_name=0)
    if "DSP" in df.columns:
        df = df[["Product Artist", "Product Title", "DSP", "Territory", "Pay"]]
    else:
        df = df[["Artist", "Track Title", "Store", "Territory", "Revenue, USD"]]
    df.columns = ["artist", "track", "platform", "country", "revenue"]
    df["report_month"] = pd.to_datetime(file_name[:7], format="%m-%Y")
    tables.append(df)

result = pd.concat(tables)

print(result.shape)
print(result["report_month"].nunique())
print(round(result["revenue"].sum(), 2))

result.sort_values("report_month").to_csv("data/interim/dsp.csv", index=False)