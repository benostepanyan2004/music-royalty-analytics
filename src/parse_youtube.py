import pandas as pd
import os


files = os.listdir("data/raw/youtube")
tables = []

for file_name in files:
    if file_name.startswith("~$"):
        continue
    df = pd.read_excel(f"data/raw/youtube/{file_name}", sheet_name="cid_audio")
    df = df[["Artist", "Album", "Revenue", "Video URL", "Payment type"]]
    df.columns = ["artist", "track", "revenue", "video_url", "payment_type"]
    df["report_month"] = pd.to_datetime(file_name[:7], format="%m-%Y")
    tables.append(df)

result = pd.concat(tables)

print(result.shape)
print(result["report_month"].nunique())
print(round(result["revenue"].sum(), 2))

result.sort_values("report_month").to_csv("data/interim/youtube.csv", index=False)
