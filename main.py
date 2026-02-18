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

def validate_products(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    :returns:
        accepted_df: accepted products dataframe
        review_df: flagged products dataframe
        reject_df: rejected products dataframe
        report: counts per rule
    :param df:
    """
    df = df.copy()

    ##################
    ## Reject rules ##
    ##################
    reject_rules = {
        "missing_id": df["id"].isna() | (df["id"].astype("string").str.strip() == ""),
        "missing_created_at": df["created_at"].isna(),
        "missing_currency": df["currency"].isna() | (df["currency"].astype("string").str.strip() == ""),
        "missing_price": df["price"].isna() ,
        "negative_price": df["price"].notna() & (df["price"] < 0)
    }
    reject_rules_df = pd.DataFrame(reject_rules)
    reject = reject_rules_df.any(axis=1)

    ##########################################
    ## Review rules (flag for human review) ##
    ##########################################
    review_rules = {
        "missing_name": df["name"].isna() | (df["name"].astype("string").str.strip() == ""),
        "price_is_zero": df["price"].notna() & (df["price"] == 0),
        "very_high_price": df["price"].notna() & (df["price"] > 30000),
    }
    review_rules_df = pd.DataFrame(review_rules)

    # Review only if its not already rejected
    to_review = (~reject) & (review_rules_df.any(axis=1))

    # Accepted if its neither rejected or review
    accepted = (~reject) & (~to_review)

    def reasons_for(mask, rules_df):
        return rules_df[mask].apply(lambda r: ",".join(r.index[r.values]), axis=1)

    rejected_df = df[reject].copy()
    rejected_df["status"] = "rejected"
    rejected_df["reason"] = reasons_for(reject, reject_rules_df)

    review_df = df[to_review].copy()
    review_df["status"] = "review"
    review_df["reason"] = reasons_for(to_review, review_rules_df)

    # Adding columns for human decision
    review_df["decision"] = pd.NA   # "accept"/"reject"
    review_df["comment"] = pd.NA   # Comment why
    review_df["reviewed_by"] = pd.NA # who did the review
    review_df["reviewed_at"] = pd.NA # Date of review

    accepted_df = df[accepted].copy()
    accepted_df["status"] = "accepted"
    accepted_df["reason"] = pd.NA


    # Report of the counts of rejects and reviews
    report = pd.DataFrame({
        "reject_count": reject_rules_df.sum(),
        "review_flag_count": review_rules_df.sum(),
    }).fillna(0).astype(int).sort_values(by=["reject_count", "review_flag_count"], ascending=False)

    return accepted_df, review_df, rejected_df, report

def build_analytics_summary(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    total_products = len(df)
    missing_price_count = df["price"].isna().sum()

    # avg and median
    avg_price = df["price"].mean()
    median_price =df["price"].median()

    summary = pd.DataFrame({
        "avg_price": [round(avg_price, 2)],
        "median_price": [round(median_price, 2)],
        "total_products": [total_products],
        "missing_price_count": [missing_price_count],
    })

    return summary

def build_price_analytics_summary(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Remove NaN
    df = df[df["price"].notna()]

    # Top 10 expensive
    top_10_expensive = (
        df.sort_values("price", ascending=False)
        .head(10)
        [["id", "name", "price"]]
        .assign(category="top_10_expensive")
    )

    # Z-score
    mean_price = df["price"].mean()
    std_price = df["price"].std()

    df["z_score"] = (df["price"] - mean_price) / std_price
    df["abs_z"] = df["z_score"].abs()

    # Top 10 outliers
    top_10_outliers = (
        df.sort_values("abs_z", ascending=False)
        .head(10)
        [["id", "name", "price", "z_score"]]
        .assign(category="top_10_outliers")
    )

    # Combine the two
    price_analysis = pd.concat([top_10_expensive, top_10_outliers])

    return price_analysis



products_df = pd.read_csv("Data/products_raw.csv", sep=";")

print(products_df)

cleaned_products_df = clean_dataframe(products_df)
print(cleaned_products_df)

accepted_df, review_df, rejected_df, report = validate_products(cleaned_products_df)


analytics_summary = build_analytics_summary(accepted_df)
price_analysis = build_price_analytics_summary(accepted_df)

analytics_summary.to_csv("Data/analytics_summary.csv", index=False)
price_analysis.to_csv("Data/price_analysis.csv", index=False)
rejected_df.to_csv("Data/rejected_products.csv", index=False)
review_df.to_csv("Data/review_df.csv", index=False)
report.to_csv("Data/reject_review_report.csv", index=False)

print(analytics_summary)
print(price_analysis)
