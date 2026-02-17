from datetime import datetime

import pandas as pd

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # PRICE: safe numeric conversion
    df["price"] = pd.to_numeric(df["price"].astype("string").str.strip(), errors="coerce")

    # NAME: normalize whitespace + title case
    df["name"] = (
        df["name"]
        .astype("string")
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
        .str.title()
    )

    # CURRENCY: strip + uppercase, keep missing as <NA>
    df["currency"] = (
        df["currency"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    # CREATED_AT: date conversion and correct formating
    df["created_at"] = (
        df["created_at"]
        .astype("string")
        .str.strip()
        .str.replace("/", "-", regex=False)
    )
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

    return df


products_df = pd.read_csv("Data/products_raw.csv", sep=";")

print(products_df)

cleaned_products_df = clean_dataframe(products_df)
print(cleaned_products_df)

##########################
##### REJECTING DATA #####
##########################

df = cleaned_products_df.copy()

# Defining reject rules
reject_rules = {
    "missing_id": df["id"].isna(),
    "missing_name": df["name"].isna(),
    "missing_currency": df["currency"].isna(),
    "missing_created_at": df["created_at"].isna(),
    "missing_price": df["price"].isna(),
    "non_positive_price": df["price"] <= 0,
}

# Creating a dataframe with rules
rules_df = pd.DataFrame(reject_rules)

# A row will be rejected if any rules are True
reject_condition = rules_df.any(axis=1)

df_rejected = df[reject_condition].copy()
df_accepted = df[~reject_condition].copy()

# Created a colum with the reason(s) for rejection
df_rejected["reject_reason"] = (
    rules_df[reject_condition]
    .apply(lambda row: ",".join(row.index[row.values]), axis=1)
)
print(df_rejected)


