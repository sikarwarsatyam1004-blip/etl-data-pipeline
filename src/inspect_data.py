import pandas as pd

file_path = "data/raw/customer_orders_raw_100k.csv"

df = pd.read_csv(file_path)

print("\nDataset Size")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nMissing Value:")
print(df.isnull().sum())

print("\nDuplicate Rows")
print(df.duplicated().sum())

print("\nData Types")
print(df.dtypes)
