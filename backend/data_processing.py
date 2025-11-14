import pandas as pd

def load_data(path="../data/books.csv"):
    df = pd.read_csv(path)
    return df


def clean_data(df):
    df = df.drop_duplicates()

    # make sure text fields are not empty
    for col in ["title", "author", "genre", "description"]:
        if col in df.columns:
            df[col] = df[col].fillna("")

    return df


def get_unique_genres(df):
    if "genre" not in df.columns:
        return []
    return sorted(df["genre"].dropna().unique())
