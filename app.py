import streamlit as st
import pickle
import requests

# ================= Custom CSS ==================== #
st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f6;
    }
    .main {
        background-color: #f0f2f6;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1 {
        color: #FF4B4B;
        text-align: center;
    }
    .css-1v0mbdj {
        text-align: center;
    }
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #D43F3F;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==================== Functions ==================== #
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=078f6f4300295e24391e10cf756c47af&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# ==================== Load Data ==================== #
movies = pickle.load(open('movies.pkl','rb'))
movies_list = movies['title'].values
similarity = pickle.load(open('similarity.pkl','rb'))

# ==================== Page Config ==================== #
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# ==================== App Title ==================== #
st.markdown("<h1>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)
st.markdown("### Discover your next favorite movie! 🍿")

# ==================== Movie Selector ==================== #
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movies_list
)

# ==================== Recommend Button ==================== #
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    st.markdown("---")
    st.markdown(f"## Because you liked **_{selected_movie}_**, you may also enjoy:")
    
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.image(recommended_movie_posters[idx], use_container_width=True)
            st.markdown(f"**{recommended_movie_names[idx]}**")

# ==================== Footer ==================== #
st.markdown(
    """
    <hr style="border:1px solid #ddd;">
    <p style="text-align: center;">📽️ Developed by Yash Kalra</p>
    """,
    unsafe_allow_html=True
)
