import streamlit as st
import pickle
import pandas as pd
import gdown
import os

# Google Drive file IDs
movie_file_id = "14_4grek2uoO7EWUijASraYbq9M4YcpMd"
similarity_file_id = "1BOOIlVtkWnvYnr_FzAv6Hg-ZJyyL9skO"

movie_path = "movie.pkl"
similarity_path = "similarity.pkl"

# Download files if not present
if not os.path.exists(movie_path):
    gdown.download(f"https://drive.google.com/uc?id={movie_file_id}", movie_path, quiet=False)

if not os.path.exists(similarity_path):
    gdown.download(f"https://drive.google.com/uc?id={similarity_file_id}", similarity_path, quiet=False)

# Load data
movies = pickle.load(open(movie_path, 'rb'))
similarity = pickle.load(open(similarity_path, 'rb'))

# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = [movies.iloc[i[0]].title for i in movies_list]
    return recommended_movies

# Streamlit UI
st.set_page_config(page_title="Movie Recommendation System", page_icon="🎬", layout="wide")

st.title("🎬 Movie Recommendation System")
st.markdown("Select a movie below and get top recommendations!")

selected_movie_name = st.selectbox(
    'Choose a movie:',
    movies['title'].values
)

if st.button('Show Recommendations'):
    recommendations = recommend(selected_movie_name)

    st.subheader("Top Recommendations:")

    cols = st.columns(len(recommendations))
    for col, movie in zip(cols, recommendations):
        with col:
            st.markdown(f"**{movie}**")
            st.image("https://via.placeholder.com/200x300?text=Movie+Poster")