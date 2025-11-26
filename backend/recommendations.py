import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_by_genre(df, genre, limit=10):
    if "genre" not in df.columns:
        return []

    # match rows where the genre field contains the selected genre
    results = df[df["genre"].str.contains(genre, case=False, na=False)]

    # return only a limited number of results
    return results.head(limit)



def recommend_random(df, limit=10):
    if len(df) == 0:
        return df

    # shuffle the rows and return the first few
    return df.sample(n=min(limit, len(df)), random_state=None)


def search_books(df, query, limit=10):
    if not query or len(df) == 0:
        return df.head(0)

    query = query.lower()

    # match in title or author
    mask = (
        df["title"].str.lower().str.contains(query, na=False) |
        df["author"].str.lower().str.contains(query, na=False)
    )

    results = df[mask]

    return results.head(limit)



def build_tfidf_matrix(df):
    if "description" not in df.columns:
        return None, None

    # turn descriptions into TF-IDF vectors
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(df["description"])

    return tfidf_matrix, vectorizer


def recommend_similar(df, tfidf_matrix, book_title, limit=10):
    if tfidf_matrix is None or "title" not in df.columns:
        return df.head(0)

    # find the row index of the selected book
    match = df[df["title"].str.lower() == book_title.lower()]
    if match.empty:
        return df.head(0)

    idx = match.index[0]

    # compute cosine similarity with all other books
    sims = cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()

    # sort by similarity (highest first), skip the book itself
    similar_indices = sims.argsort()[::-1][1 : limit + 1]

    return df.iloc[similar_indices]
