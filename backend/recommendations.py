def recommend_by_genre(df, genre, limit=10):
    if "genre" not in df.columns:
        return []

    # match rows where the genre field contains the selected genre
    results = df[df["genre"].str.contains(genre, case=False, na=False)]

    # return only a limited number of results
    return results.head(limit)
