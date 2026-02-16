from datetime import datetime

import pandas as pd

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # --- PRICE: safe numeric conversion
    df["price"] = pd.to_numeric(df["price"].astype("string").str.strip(), errors="coerce")

    # --- NAME: normalize whitespace + title case
    df["name"] = (
        df["name"]
        .astype("string")
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
        .str.title()
    )

    # --- CURRENCY: strip + uppercase, keep missing as <NA>
    df["currency"] = (
        df["currency"]
        .astype("string")
        .str.strip()
        .str.upper()
    )
    df["created_at"] = (
        pd.to_datetime(df["created_at"], errors="coerce")
        .dt.strftime("%Y-%m-%d")
    )

    return df


products_df = pd.read_csv("Data/products_raw.csv", sep=";")

print(products_df)

cleaned_products_df = clean_dataframe(products_df)
print(cleaned_products_df)

reject_condition = (
    cleaned_products_df["id"].isna() |
    cleaned_products_df["name"].isna() |
    cleaned_products_df["currency"].isna() |
    cleaned_products_df["created_at"].isna() |
    cleaned_products_df["price"].isna() | (cleaned_products_df["price"] <= 0)
)

df_rejected = cleaned_products_df[reject_condition].copy()
df_accepted = cleaned_products_df[~reject_condition].copy()

print(df_accepted)
print(df_rejected)
