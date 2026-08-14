import pandas as pd

cleaned_file = "data/processed/cleaned_orders.csv"
rejected_file = "data/processed/rejected_orders.csv"

clean_df = pd.read_csv(cleaned_file)
rejected_df = pd.read_csv(rejected_file)

print("Cleaned Data Shape:")
print(clean_df.shape)

print("\nRejected Data Shape:")
print(rejected_df.shape)

print("\nMissing Values in Cleaned Data:")
print(clean_df.isnull().sum())

print("\nDuplicates in Cleaned Data:")
print(clean_df.duplicated().sum())

print("\nRejection Reasons:")
print(rejected_df["rejection_reason"].value_counts())

print("\nSample Rejected Records:")

print(
    rejected_df[
        ["order_id", "order_date", "order_status", "rejection_reason"]
    ].head(10)
)