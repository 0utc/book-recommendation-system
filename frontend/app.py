import streamlit as st
import pandas as pd
import sys
import os

# Add backend folder to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

# Import backend functions
from data_processing import load_data, clean_data, get_unique_genres
from recommendations import (
    recommend_by_genre,
    recommend_random,
    search_books,
    build_tfidf_matrix,
    recommend_similar
)

# Constants
MAX_RESULTS = 10

# Streamlit page setup
st.set_page_config(
    page_title="Book Recommendation System - University Project",
    page_icon="📚",
    layout="centered"
)

# Header
st.title("📚 Book Recommendation System - University Project")
st.markdown("---")

# Load and prepare data
@st.cache_data
def load_and_prepare_data():
    try:
        df = load_data("../data/books.csv")
        df = clean_data(df)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_and_prepare_data()

# Build TF-IDF matrix once
@st.cache_resource
def get_tfidf_matrix(df):
    tfidf_matrix, vectorizer = build_tfidf_matrix(df)
    return tfidf_matrix, vectorizer

if not df.empty:
    tfidf_matrix, _ = get_tfidf_matrix(df)

    # Data overview
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Books", len(df))
    with col2:
        genres = get_unique_genres(df)
        st.metric("Genres", len(genres))
    with col3:
        st.metric("Authors", df['author'].nunique())

    st.markdown("---")

    # 🔍 Search Section
    st.subheader("🔍 Quick Search")
    search_query = st.text_input("Search for a book or author:", placeholder="Type a keyword...")
    search_limit = st.number_input("Max results", min_value=1, max_value=MAX_RESULTS, value=MAX_RESULTS)

    if search_query:
        search_results = search_books(df, search_query, limit=search_limit)
        if not search_results.empty:
            st.write(f"**Search Results ({len(search_results)} books):**")
            # Select a book for similar recommendations
            selected_title = st.selectbox(
                "Select a book to see similar recommendations:",
                ["Select a book..."] + search_results["title"].tolist()
            )
            for i, row in search_results.iterrows():
                st.write(f"📗 **{row['title']}** by {row['author']}")
                st.write(f"**Genre:** {row['genre']}")
                st.write(f"**Description:** {row['description'][:200]}...")
                st.markdown("---")

            if selected_title != "Select a book...":
                similar = recommend_similar(df, tfidf_matrix, selected_title, limit=5)
                if not similar.empty:
                    st.write("**Similar Books:**")
                    for _, sim_row in similar.iterrows():
                        st.write(f"- {sim_row['title']} ({sim_row['author']})")
        else:
            st.info("No results found.")

    st.markdown("---")

    # 📂 Browse by Genre
    st.subheader("📂 Browse by Genre")
    if genres:
        selected_genre = st.selectbox("Choose a genre:", ["Select..."] + genres)
        genre_limit = st.number_input("Max results", min_value=1, max_value=MAX_RESULTS, value=MAX_RESULTS, key="genre_limit")

        if selected_genre != "Select...":
            genre_books = recommend_by_genre(df, selected_genre, limit=genre_limit)
            if not genre_books.empty:
                st.write(f"**Books in {selected_genre} ({len(genre_books)} shown):**")
                for _, row in genre_books.iterrows():
                    st.write(f"📗 **{row['title']}**")
                    st.write(f"👤 Author: {row['author']}")
                    st.write(f"📝 {row['description'][:100]}...")
                    st.markdown("---")
            else:
                st.info(f"No books found in {selected_genre}.")

    st.markdown("---")

    # 🎲 Random Recommendations
    st.subheader("🎲 Discover Random Books")
    if st.button("🔄 Show Random Books"):
        random_limit = st.number_input("Max results", min_value=1, max_value=MAX_RESULTS, value=MAX_RESULTS, key="random_limit")
        random_books = recommend_random(df, limit=random_limit)
        if not random_books.empty:
            st.write(f"**Random Book Suggestions ({len(random_books)} books):**")
            for i, row in random_books.iterrows():
                st.write(f"📗 **{row['title']}** by {row['author']} ({row['genre']})")
                st.markdown("---")

    st.markdown("---")

    # 📊 Basic Data Insights
    st.subheader("📊 Basic Data Insights")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Top Genres:**")
        genre_counts = df['genre'].value_counts().head(5)
        for genre, count in genre_counts.items():
            st.write(f"- {genre}: {count} books")
    with col2:
        st.write("**Most Active Authors:**")
        author_counts = df['author'].value_counts().head(5)
        for author, count in author_counts.items():
            st.write(f"- {author}: {count} books")

# Footer
st.markdown("---")
st.markdown("### 👥 Project Info")
st.write("**Project:** Book Recommendation System")
st.write("**Backend:** Oussama Aissati")
st.write("**Frontend:** Bouich Mohamed")
st.write(f"**Maximum books per request:** {MAX_RESULTS}")
