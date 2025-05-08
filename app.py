import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie poster
def fetch_poster(movie_id):
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=7bd9dd4627d7ac2c386b1be4a005ebae',
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
        else:
            return "https://via.placeholder.com/300x450?text=No+Poster"
    except Exception as e:
        print(f"Error fetching poster for movie_id {movie_id}: {e}")
        return "https://via.placeholder.com/300x450?text=Error"

# Function to recommend similar movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters

# Load the movie data and similarity matrix from pickle files
try:
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    movies = pickle.load(open('movies.pkl', 'rb'))
except FileNotFoundError:
    st.error("Pickle files (similarity.pkl and movies.pkl) are missing. Please check.")
    st.stop()

movies_list_name = movies['title'].values

# Streamlit UI setup
st.set_page_config(page_title="Movie Recommender", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }
    .main {
        background-color: #0e1117;
    }
    h1 {
        text-align: center;
        color: #f9a826;
    }
    .stSelectbox label {
        color: white !important;
    }
    .stButton>button {
        background-color: #f9a826;
        color: black;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5em 2em;
        border: none;
    }
    .stButton>button:hover {
        background-color: #ffd369;
        color: black;
    }
    .stImage img {
        border-radius: 12px;
        box-shadow: 0px 0px 15px rgba(255,255,255,0.2);
        transition: 0.3s ease-in-out;
    }
    .stImage img:hover {
        transform: scale(1.05);
    }
    h3 {
        color: #f0f0f0;
        text-align: center;
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title('🎬 Movie Recommender System')

# Movie selection
selected_movie_name = st.selectbox('Select a Movie to recommend', movies_list_name)

# Recommendation output
if st.button('Recommend Movie'):
    if selected_movie_name:
        recommendations, posters = recommend(selected_movie_name)

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.markdown(f"### {recommendations[0]}")
            st.image(posters[0])
        with col2:
            st.markdown(f"### {recommendations[1]}")
            st.image(posters[1])
        with col3:
            st.markdown(f"### {recommendations[2]}")
            st.image(posters[2])
        with col4:
            st.markdown(f"### {recommendations[3]}")
            st.image(posters[3])
        with col5:
            st.markdown(f"### {recommendations[4]}")
            st.image(posters[4])
    else:
        st.error("Please select a movie to get recommendations.")
