import pandas as pd
import os


files = os.listdir("data/raw/dsp")
tables = []

files_read = 0
months = []
expected_rows = 0
expected_revenue = 0

for file_name in files:
    if file_name.startswith("~$"):
        continue
    df = pd.read_excel(f"data/raw/dsp/{file_name}", sheet_name=0)

    files_read += 1
    expected_rows += len(df)

    if "DSP" in df.columns:
        expected_revenue += df["Pay"].sum()
        df = df[["Product Artist", "Product Title", "Asset ISRC", "Product UPC", "DSP", "Territory", "Pay"]]
    else:
        expected_revenue += df["Revenue, USD"].sum()
        df = df[["Artist", "Track Title", "ISRC", "UPC", "Store", "Territory", "Revenue, USD"]]
    df.columns = ["artist", "track", "isrc", "upc", "platform", "country", "revenue"]
    report_month = pd.to_datetime(file_name[:7], format="%m-%Y")
    df["report_month"] = report_month
    months.append(report_month)
    tables.append(df)

result = pd.concat(tables)
result.sort_values("report_month").to_csv("data/interim/dsp.csv", index=False)

all_months = pd.date_range(min(months), max(months), freq="MS")

# Read the saved file back and compare it with the source files
check = pd.read_csv("data/interim/dsp.csv")
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