import pandas as pd
import numpy as np

def clean_data(raw_data.csv):
    df = pd.read_csv(raw_data.csv)

    print("Initial Shape:", df.shape)

    # -------------------------
    # 1. Handle Missing Values
    # -------------------------
    for col in df.columns:
        if df[col].dtype == "object":
            df[col].fillna(df[col].mode()[0], inplace=True)
        else:
            df[col].fillna(df[col].median(), inplace=True)

    # -------------------------
    # 2. Remove Duplicates
    # -------------------------
    df.drop_duplicates(inplace=True)

    # -------------------------
    # 3. Handle Outliers (IQR)
    # -------------------------
    numeric_cols = df.select_dtypes(include=np.number).columns

    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        df[col] = np.clip(df[col], lower, upper)

    # -------------------------
    # 4. Standardize Text
    # -------------------------
    text_cols = df.select_dtypes(include="object").columns
    for col in text_cols:
        df[col] = df[col].str.strip().str.lower()

    # -------------------------
    # 5. Date Formatting
    # -------------------------
    for col in df.columns:
        try:
            df[col] = pd.to_datetime(df[col])
        except:
            pass

    print("Final Shape:", df.shape)

    return df


if __name__ == "__main__":
    cleaned_df = clean_data("data/raw_data.csv")
    cleaned_df.to_csv("output/cleaned_data.csv", index=False)
    print("Cleaning completed successfully!")