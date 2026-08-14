import pandas as pd

file_path = "data/raw/customer_orders_raw_100k.csv"

df = pd.read_csv(file_path)

print("Before cleaning:")
print(df.shape)

df = df.drop_duplicates()

print("\nAfter Removing Duplicates:")
print(df.shape)

df["email"] = df["email"].fillna("unknown@example.com")
df["city"] = df["city"].fillna("Unknown")
df["age"] = df["age"].fillna(df["age"].median())
df["state"] = df["state"].fillna("Unknown")
df["unit_price"] = df["unit_price"].fillna(df["unit_price"].median())
df["payment_method"] = df["payment_method"].fillna("Unknown")

df["total_amount"] = df["total_amount"].fillna(
    df["quantity"] * df["unit_price"]
)

print("\nmissing Values After Cleaning:")
print(df.isnull().sum())

df["order_date"] = pd.to_datetime(
    df["order_date"],
    errors="coerce"
)

email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

df["valid_email"] = df["email"].str.match(
    email_pattern,
    na=False
)

print(df["valid_email"].value_counts())

df.loc[~df["valid_email"], "email"] = "unknown@example.com"

df["valid_email"] = df["email"].str.match(
    email_pattern,
    na=False
)

print("\nEmail Validation After Cleaning:")
print(df["valid_email"].value_counts())

print("\nAge Statistics:")
print(df["age"].describe())

invalid_age = ~df["age"].between(18, 100)

print("\nInvalid Age Records:")
print(invalid_age.sum())


valid_age_median = df.loc[
    df["age"].between(18,100),
    "age"
].median()

df.loc[invalid_age, "age"] = valid_age_median
df["age"] = df["age"].astype(int)

print("\nInvalid Ages After Cleaning:")
print((~df["age"].between(18,100)).sum())


invalid_quantity = df["quantity"] <=0

print("\nInvalid Quantity Records:")
print(invalid_quantity.sum())

df.loc[invalid_quantity, "quantity"] = 1

print("\nInvalid Quanties After Cleaning:")
print((df["quantity"] <= 0).sum())


invalid_price = df["unit_price"] <= 0

print("\nInvalid Unit Price Records:")
print(invalid_price.sum ())

invalid_discount = ~df["discount_pct"].between(0,100)

print("\nInvalid Discount Records:")
print(invalid_discount.sum())

invalid_dates = df["order_date"].isna()

print("\nInvalid Order Date Record:")
print(invalid_dates.sum())

print("\nOrder Status Values:")
print(df["order_status"].value_counts())


df["order_status"] = df["order_status"].replace({
    "complete": "Completed",
    "SHIPPED": "Shipped"
})


valid_statuses = [
    "Completed",
    "Processing",
    "Cancelled",
    "Shipped",
    "Returned"
]

invalid_status = ~df["order_status"].isin(valid_statuses)

print("\nInvalid Order Status Records:")
print(invalid_status.sum())


df["calculated_total"] = (
    df["quantity"]
    * df["unit_price"]
    * (1 - df["discount_pct"] / 100)
).round(2)

invalid_total = (
    df["total_amount"].round(2)
    != df["calculated_total"]
)

print("\nIncorrect Total Amount Records:")
print(invalid_total.sum())


df.loc[invalid_total, "total_amount"] = df.loc[
    invalid_total,
    "calculated_total"
]

invalid_total_after = (
    df["total_amount"].round(2)
    != df["calculated_total"]
)

print("\nIncorrect Totals After Cleaning:")
print(invalid_total_after.sum())


rejected_condition = (
    df["order_date"].isna()
    | ~df["order_status"].isin(valid_statuses)
)

print("\nRejected Records:")
print(rejected_condition.sum())

print("\nValid Records:")
print((~rejected_condition).sum())



valid_df = df[~rejected_condition].copy()

rejected_df = df[rejected_condition].copy()

rejected_df["rejection_reason"] = ""

rejected_df.loc[
    rejected_df["order_date"].isna(),
    "rejection_reason"
] = "INVALID_ORDER_DATE"

rejected_df.loc[
    ~rejected_df["order_status"].isin(valid_statuses),
    "rejection_reason"
] = "INVALID_ORDER_STATUS"

print("\nFinal Valid DataFrame:")
print(valid_df.shape)

print("\nFinal Rejected DataFrame:")
print(rejected_df.shape)


valid_df = valid_df.drop(
    columns=["valid_email", "calculated_total"]
)

rejected_df = rejected_df.drop(
    columns=["valid_email", "calculated_total"]
)


print("\nValid Data Final Shape:")
print(valid_df.shape)

print("\nRejected Data Final Shape:")
print(rejected_df.shape)

valid_df.to_csv(
    "data/processed/cleaned_orders.csv",
    index=False
)

rejected_df.to_csv(
    "data/processed/rejected_orders.csv",
    index=False
)

print("\nFiles saved successfully.")
