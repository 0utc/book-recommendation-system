import streamlit as st
import pandas as pd
import sys
import os

# Add backend folder to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

from data_processing import load_data, clean_data, get_unique_genres
from recommendations import (
    recommend_by_genre,
    recommend_random,
    search_books,
    build_tfidf_matrix,
    recommend_similar
)

# Streamlit page setup
st.set_page_config(
    page_title="Book Recommendation System - University Project",
    page_icon="📚",
    layout="centered"
)

st.title("📚 Book Recommendation System - University Project")
st.markdown("---")

@st.cache_data
# Load and clean dataset once to improve performance
def load_and_prepare_data():
    try:
        # Correct path relative to this file (frontend/app.py)
        DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'books.csv'))
        df = load_data(DATA_PATH)
        df = clean_data(df)
        return df
    except FileNotFoundError:
        st.error(f"Data file not found at {DATA_PATH}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

@st.cache_data
# Build and cache TF-IDF matrix for content-based recommendations
def get_cached_tfidf(df):
    if df.empty:
        return None, None
    return build_tfidf_matrix(df)

# Load data
df = load_and_prepare_data()

if df.empty:
    st.warning("No data available. Make sure books.csv exists in the data/ folder.")
else:
    # Used later to compute similarity between books
    tfidf_matrix, vectorizer = get_cached_tfidf(df)
    
    # Basic metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Books", len(df))
    with col2:
        genres = get_unique_genres(df)
        st.metric("Genres", len(genres))
    with col3:
        st.metric("Authors", df['author'].nunique())

    st.markdown("---")

    # Quick Search
    st.subheader("🔍 Quick Search")
    col_search1, col_search2 = st.columns([4, 1])
    with col_search1:
        search_query = st.text_input("Search for a book or author:", placeholder="Type a keyword...")
    with col_search2:
        search_limit = st.number_input("Max", min_value=1, max_value=10, value=10, key="search_limit", help="Max: 10 books")
    
    if search_query:
        search_results = search_books(df, search_query, limit=search_limit)
        if not search_results.empty:
            st.write(f"**Search Results ({len(search_results)} books):**")
            for i, row in search_results.iterrows():
                with st.expander(f"{row['title']} - {row['author']}"):
                    st.write(f"**Genre:** {row['genre']}")
                    st.write(f"**Description:** {row['description'][:200]}...")
                    if st.button(f"📖 Similar books to {row['title']}", key=f"similar_{i}"):
                        if tfidf_matrix is not None:
                            similar = recommend_similar(df, tfidf_matrix, row['title'], 5)
                            st.write("**Similar Books:**")
                            for _, sim_row in similar.iterrows():
                                st.write(f"- {sim_row['title']} ({sim_row['author']})")
                        else:
                            st.info("Content analysis not available.")
        else:
            st.info("No results found.")

    st.markdown("---")

    # Browse by Genre
    st.subheader("📂 Browse by Genre")
    if genres:
        col_genre1, col_genre2 = st.columns([4, 1])
        with col_genre1:
            selected_genre = st.selectbox("Choose a genre:", ["Select..."] + genres, key="genre_select")
        with col_genre2:
            genre_limit = st.number_input("Max", min_value=1, max_value=10, value=10, key="genre_limit", help="Max: 10 books")
        
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

    # Random Recommendations
    st.subheader("🎲 Discover Random Books")
    col_random1, col_random2 = st.columns([3, 1])
    with col_random1:
        if st.button("🔄 Show New Random Books", key="random_btn"):
            st.session_state.show_random = True
    with col_random2:
        random_limit = st.number_input("Max", min_value=1, max_value=10, value=10, key="random_limit", help="Max: 10 books")
    
    if 'show_random' not in st.session_state:
        st.session_state.show_random = False
    
    if st.session_state.show_random:
        random_books = recommend_random(df, limit=random_limit)
        if not random_books.empty:
            st.write(f"**Random Book Suggestions ({len(random_books)} books):**")
            for i, row in random_books.iterrows():
                col_book1, col_book2 = st.columns([4, 1])
                with col_book1:
                    st.write(f"📗 **{i+1}. {row['title']}**")
                    st.write(f"👤 Author: {row['author']}")
                    st.write(f"📝 Genre: {row['genre']}")
                st.markdown("---")

    st.markdown("---")
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

st.markdown("---")
st.markdown("### 👥 Project Info")
st.write("**Project:** Book Recommendation System")
st.write("**Backend:** Oussama Aissati")
st.write("**Frontend:** Bouich Mohamed")
