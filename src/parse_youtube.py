import pandas as pd
import os


files = os.listdir("data/raw/youtube")
tables = []

files_read = 0
months = []
expected_rows = 0
expected_revenue = 0

for file_name in files:
    if file_name.startswith("~$"):
        continue
    df = pd.read_excel(f"data/raw/youtube/{file_name}", sheet_name="cid_audio")

    files_read += 1
    expected_rows += len(df)
    expected_revenue += df["Revenue"].sum()

    df = df[["Artist", "Album", "ISRC", "UPC", "Revenue", "Video URL", "Payment type"]]
    df.columns = ["artist", "track", "isrc", "upc", "revenue", "video_url", "payment_type"]
    report_month = pd.to_datetime(file_name[:7], format="%m-%Y")
    df["report_month"] = report_month
    months.append(report_month)
    tables.append(df)

result = pd.concat(tables)
result.sort_values("report_month").to_csv("data/interim/youtube.csv", index=False)

# Every month from the first to the last report
all_months = pd.date_range(min(months), max(months), freq="MS")

check = pd.read_csv("data/interim/youtube.csv")
assert len(months) == len(set(months)), "two reports for the same month"
assert files_read == len(all_months), "a month is missing between the first and the last report"
assert len(check) == expected_rows, "row count does not match the source files"
assert round(check["revenue"].sum(), 2) == round(expected_revenue, 2), "revenue does not match the source files"

print("Reports:", files_read)
print("First report:", f"{min(months):%m-%Y}")
print("Last report:", f"{max(months):%m-%Y}")
print("Rows:", len(check))
print("Revenue:", round(check["revenue"].sum(), 2))
print("All checks passed")