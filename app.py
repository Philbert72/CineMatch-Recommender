import streamlit as st
import pickle
import requests
import pandas as pd
from typing import List, Tuple, Dict
import time
import re
import datetime
import threading

# Page configuration
st.set_page_config(
    page_title="🎬 CineMatch",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark streaming platform look
st.markdown("""
<style>
    /* Global styles */
    .stApp {
        background-color: #0f1117;
        color: #ffffff;
    }
    
    /* Header styles */
    .main-header {
        display: flex;
        align-items: center;
        color: white;
        font-size: 2.2rem;
        font-weight: bold;
        margin-bottom: 1rem;
        padding: 0.5rem 0;
    }
    
    /* Navigation bar */
    .nav-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 1rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 1.5rem;
    }
    
    .search-container {
        width: 100%;
        max-width: 800px;
        position: relative;
    }
    
    /* Movie card styles */
    .movie-card {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        overflow: hidden;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .movie-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
    }
    
    .movie-info {
        padding: 0.8rem;
    }
    
    .movie-title {
        color: white;
        font-weight: bold;
        font-size: 1rem;
        margin-bottom: 0.3rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .movie-meta {
        display: flex;
        align-items: center;
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.8rem;
    }
    
    .rating {
        color: #ffd700;
        margin-right: 0.5rem;
    }
    
    /* Section titles */
    .section-title {
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 2rem 0 1rem 0;
        display: flex;
        align-items: center;
    }
    
    /* Featured section */
    .featured-container {
        position: relative;
        margin-bottom: 2rem;
    }
    
    .featured-info {
        position: absolute;
        bottom: 0;
        left: 0;
        padding: 2rem;
        background: linear-gradient(transparent, rgba(0,0,0,0.8) 50%, rgba(0,0,0,0.9));
        width: 100%;
    }
    
    .featured-title {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .featured-description {
        font-size: 1rem;
        margin-bottom: 1rem;
        max-width: 600px;
    }
    
    /* Button styles */
    .watch-button {
        background-color: rgba(255, 255, 255, 0.2);
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 5px;
        font-weight: bold;
        cursor: pointer;
        transition: background-color 0.3s ease;
        display: inline-flex;
        align-items: center;
    }
    
    .watch-button:hover {
        background-color: rgba(255, 255, 255, 0.3);
    }
    
    /* Back button */
    .back-button {
        background-color: rgba(61, 133, 198, 0.7);
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 5px;
        font-weight: bold;
        cursor: pointer;
        transition: background-color 0.3s ease;
        display: inline-flex;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .back-button:hover {
        background-color: rgba(61, 133, 198, 0.9);
    }
    
    /* Hide Streamlit elements */
    #MainMenu, footer, header {
        visibility: hidden;
    }
    
    /* Genre section */
    .genre-title {
        border-left: 4px solid #3d85c6;
        padding-left: 0.8rem;
        margin: 2rem 0 1rem 0;
    }
    
    /* Trending section */
    .trending-title {
        border-left: 4px solid #e74c3c;
        padding-left: 0.8rem;
        margin: 2rem 0 1rem 0;
    }
    
    /* Action section */
    .action-title {
        border-left: 4px solid #e67e22;
        padding-left: 0.8rem;
        margin: 2rem 0 1rem 0;
    }
    
    /* Comedy section */
    .comedy-title {
        border-left: 4px solid #2ecc71;
        padding-left: 0.8rem;
        margin: 2rem 0 1rem 0;
    }
    
    /* Horror section */
    .horror-title {
        border-left: 4px solid #9b59b6;
        padding-left: 0.8rem;
        margin: 2rem 0 1rem 0;
    }
    
    /* Drama section */
    .drama-title {
        border-left: 4px solid #f1c40f;
        padding-left: 0.8rem;
        margin: 2rem 0 1rem 0;
    }
    
    /* Search results */
    .search-results-container {
        margin: 2rem 0;
    }
    
    .search-results-title {
        color: white;
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .search-movie-card {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        overflow: hidden;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
        cursor: pointer;
        height: 100%;
    }
    
    .search-movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
    }
    
    /* Recommendation results */
    .recommendation-result {
        background-color: rgba(61, 133, 198, 0.1);
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid rgba(61, 133, 198, 0.3);
    }
    
    /* Custom selectbox */
    div[data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 5px;
    }
    
    /* Custom button */
    .stButton > button {
        background-color: #3d85c6;
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 5px;
        font-weight: bold;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: #5294d0;
    }
    
    /* Custom text input */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 25px;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.5);
    }
    
    /* Spinner */
    .stSpinner > div > div {
        border-top-color: #3d85c6 !important;
    }

    /* Back button styling */
    .back-button-container {
        margin: 1rem 0;
    }

    .stButton > button[data-testid="back_button"] {
        background-color: rgba(61, 133, 198, 0.7);
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 5px;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }

    .stButton > button[data-testid="back_button"]:hover {
        background-color: rgba(61, 133, 198, 0.9);
    }

    /* Arrow button styles */
    .arrow-vertical-center {
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 500px;
    }

    .arrow-vertical-center .stButton > button {
        border: none !important;
        outline: none !important;
        background: transparent !important;
        color: white !important;
        font-size: 2.5rem;
        width: 56px;
        height: 56px;
        border-radius: 50%;
        box-shadow: none !important;
        margin: 0;
        padding: 0;
        transition: background 0.2s;
        opacity: 1;
    }

    .arrow-vertical-center .stButton > button:hover {
        background: rgba(255,255,255,0.08) !important;
        color: #ffd700 !important;
        opacity: 1;
    }

    /* Remove any border or background from the button's focus state as well */
    .arrow-vertical-center .stButton > button:focus {
        border: none !important;
        outline: none !important;
        background: transparent !important;
        box-shadow: none !important;
    }
</style>
""", unsafe_allow_html=True)

def format_rating(rating):
    """Format rating to show only 1 decimal place"""
    if rating is None or rating == 'N/A':
        return 'N/A'
    try:
        # Convert to float and round to 1 decimal place
        return f"{float(rating):.1f}"
    except (ValueError, TypeError):
        return 'N/A'

@st.cache_data
def load_data():
    """Load pickle files with caching for better performance"""
    try:
        movies = pickle.load(open("movies_list.pkl", 'rb'))
        similarity = pickle.load(open("similarity.pkl", 'rb'))
        return movies, similarity
    except Exception as e:
        st.error(f"❌ Error loading data files: {e}")
        st.info("Please ensure 'movies_list.pkl' and 'similarity.pkl' are in the same directory")
        st.stop()

@st.cache_data
def fetch_poster(movie_id: int) -> str:
    """Fetch movie poster with caching and error handling"""
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=06dfaf242c2b13648135a0e747b743e9&language=en-US"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'poster_path' in data and data['poster_path']:
            return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"
    except Exception as e:
        return "https://via.placeholder.com/500x750?text=Poster+Unavailable"

@st.cache_data
def get_movie_details(movie_id: int) -> dict:
    """Fetch additional movie details"""
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=YOUR_TMDB_API_KEY_HERE"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except:
        return {}

@st.cache_data
def get_genre_movies(genre_id: int, limit: int = 5) -> List[dict]:
    """Fetch movies by genre"""
    try:
        url = f"https://api.themoviedb.org/3/discover/movie?api_key=06dfaf242c2b13648135a0e747b743e9&with_genres={genre_id}&sort_by=popularity.desc"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        movies = response.json().get('results', [])[:limit]
        
        # Enhance with additional details
        for movie in movies:
            movie['details'] = get_movie_details(movie['id'])
            movie['poster'] = fetch_poster(movie['id'])
            
        return movies
    except Exception as e:
        return []

def search_movies_with_details(query: str, movies_df: pd.DataFrame, limit: int = 12) -> List[dict]:
    """Search for movies and return with details including posters"""
    if not query:
        return []
    
    query_lower = query.lower().strip()
    
    # Find all movies that contain the search term
    matching_movies = movies_df[movies_df['title'].str.lower().str.contains(query_lower, na=False)]
    
    # Limit results
    matching_movies = matching_movies.head(limit)
    
    results = []
    for _, movie in matching_movies.iterrows():
        movie_details = get_movie_details(movie['id'])
        results.append({
            'id': movie['id'],
            'title': movie['title'],
            'poster': fetch_poster(movie['id']),
            'details': movie_details
        })
    
    return results

def recommend(movie: str, movies_df: pd.DataFrame, similarity_matrix) -> Tuple[List[str], List[str], List[dict]]:
    """Enhanced recommendation function with additional movie details"""
    try:
        index = movies_df[movies_df['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity_matrix[index])), reverse=True, key=lambda x: x[1])
        
        recommend_movies = []
        recommend_posters = []
        movie_details = []
        
        for i in distances[1:6]:  # Top 5 recommendations
            movie_id = movies_df.iloc[i[0]].id
            movie_title = movies_df.iloc[i[0]].title
            
            recommend_movies.append(movie_title)
            recommend_posters.append(fetch_poster(movie_id))
            movie_details.append(get_movie_details(movie_id))
            
        return recommend_movies, recommend_posters, movie_details
    except Exception as e:
        st.error(f"Error generating recommendations: {e}")
        return [], [], []

def display_featured_movies_carousel():
    """Display a carousel of featured movies with left/right navigation arrows vertically centered next to the image, and auto-advance every 5 seconds using Streamlit's rerun."""
    featured_ids = [299536, 155, 240, 429422, 17455]
    if 'featured_index' not in st.session_state:
        st.session_state.featured_index = 0
    if 'carousel_last_update' not in st.session_state:
        st.session_state.carousel_last_update = time.time()

    # Auto-advance every 5 seconds (Streamlit-friendly way)
    now = time.time()
    if now - st.session_state.carousel_last_update > 5:
        st.session_state.featured_index = (st.session_state.featured_index + 1) % len(featured_ids)
        st.session_state.carousel_last_update = now
        # Use st.rerun() for Streamlit >=1.25, fallback to experimental_rerun for older versions
        try:
            st.rerun()
        except AttributeError:
            st.experimental_rerun()

    new_index = st.session_state.featured_index

    # Custom CSS to vertically center the buttons in their columns
    st.markdown('''
    <style>
    .arrow-vertical-center {
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 500px;
    }
    </style>
    ''', unsafe_allow_html=True)

    col_left, col_center, col_right = st.columns([1, 8, 1], gap="small")

    # Vertically center the arrow buttons with the featured movie image
    with col_left:
        st.markdown('<div style="display:flex; align-items:center; height:500px;"><div style="margin:auto;">', unsafe_allow_html=True)
        left_btn = st.button('←', key='featured_left', help='Previous', use_container_width=True)
        st.markdown('</div></div>', unsafe_allow_html=True)
    with col_right:
        st.markdown('<div style="display:flex; align-items:center; height:500px;"><div style="margin:auto;">', unsafe_allow_html=True)
        right_btn = st.button('→', key='featured_right', help='Next', use_container_width=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    if left_btn:
        new_index = (st.session_state.featured_index - 1) % len(featured_ids)
    if right_btn:
        new_index = (st.session_state.featured_index + 1) % len(featured_ids)
    st.session_state.featured_index = new_index

    featured_id = featured_ids[new_index]
    featured_details = get_movie_details(featured_id)
    backdrop_url = f"https://image.tmdb.org/t/p/original{featured_details.get('backdrop_path', '')}" if featured_details.get('backdrop_path') else fetch_poster(featured_id)
    formatted_rating = format_rating(featured_details.get('vote_average', 8.2))

    with col_center:
        st.markdown(f'''
        <div class="featured-container">
            <img src="{backdrop_url}" style="width:100%; height:500px; object-fit:cover; object-position:center; border-radius:10px;">
            <div class="featured-info">
                <div class="featured-title">{featured_details.get('title', 'Featured Movie')}</div>
                <div class="featured-description">{featured_details.get('overview', '')[:200]}...</div>
                <div class="movie-meta">
                    <span class="rating">⭐ {formatted_rating}/10</span>
                    <span>📅 {featured_details.get('release_date', 'N/A')[:4]}</span>
                    <span style="margin-left:10px;">⏱️ {featured_details.get('runtime', 'N/A')}min</span>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

def display_movie_section(movies, title, title_class):
    """Display a section of movies with a title"""
    if not movies:
        return
    
    st.markdown(f'<div class="{title_class} section-title">{title}</div>', unsafe_allow_html=True)
    
    # Create a container for the movies
    cols = st.columns(5)
    
    for i, movie in enumerate(movies[:5]):  # Limit to 5 movies per row
        with cols[i % 5]:
            # Format the rating
            formatted_rating = format_rating(movie.get('vote_average') or movie.get('details', {}).get('vote_average'))
            
            # Get release year
            if 'release_date' in movie:
                year = movie.get('release_date', '')[:4] if movie.get('release_date') else 'N/A'
            else:
                year = movie.get('details', {}).get('release_date', '')[:4] if movie.get('details', {}).get('release_date') else 'N/A'
            
            # Get poster
            poster = movie.get('poster') or movie.get('poster_path')
            if not poster:
                if 'poster_path' in movie:
                    poster = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie['poster_path'] else "https://via.placeholder.com/500x750?text=No+Poster+Available"
            
            # Get title
            title = movie.get('title', 'N/A')
            
            st.markdown(f"""
            <div class="movie-card">
                <img src="{poster}" style="width:100%; aspect-ratio:2/3; object-fit:cover;">
                <div class="movie-info">
                    <div class="movie-title">{title}</div>
                    <div class="movie-meta">
                        <span class="rating">⭐ {formatted_rating}</span>
                        <span>📅 {year}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def display_trending_movies(movies_df):
    """Display trending movies in a horizontal scroll"""
    trending_ids = [1632, 299536, 17455, 2830, 429422, 9722, 13972, 240, 155]
    
    trending_movies = []
    for movie_id in trending_ids:
        # Find movie in dataset
        movie_row = movies_df[movies_df['id'] == movie_id]
        if not movie_row.empty:
            movie_title = movie_row.iloc[0]['title']
            details = get_movie_details(movie_id)
            poster = fetch_poster(movie_id)
            
            trending_movies.append({
                'id': movie_id,
                'title': movie_title,
                'details': details,
                'poster': poster
            })
    
    display_movie_section(trending_movies, "Trending", "trending-title")

def display_genre_sections():
    """Display movie sections by genre"""
    # Define genres with their TMDB IDs
    genres = {
        'Action': 28,
        'Comedy': 35,
        'Horror': 27,
        'Drama': 18
    }
    
    # Display each genre section
    for genre_name, genre_id in genres.items():
        genre_movies = get_genre_movies(genre_id)
        display_movie_section(genre_movies, genre_name, f"{genre_name.lower()}-title")

def display_search_results(search_results):
    """Display search results with movie posters in a grid"""
    if not search_results:
        return
    
    # Add back button at the top of search results
    if st.button("← Back to Home", key="back_button"):
        st.session_state.show_search_results = False
        st.session_state.search_query = ""
        # Clear the search input
        
        try:
            st.rerun()
        except AttributeError:
            # Fallback for older Streamlit versions
            st.experimental_rerun()
    
    # Rest of the search results display code...
    
    st.markdown(f"""
    <div class="search-results-container">
        <div class="search-results-title">Search Results ({len(search_results)} movies found)</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display results in a grid
    cols = st.columns(4)
    
    for i, movie in enumerate(search_results):
        with cols[i % 4]:
            # Display movie card
            formatted_rating = format_rating(movie['details'].get('vote_average'))
            year = movie['details'].get('release_date', '')[:4] if movie['details'].get('release_date') else 'N/A'
            
            st.markdown(f"""
            <div class="search-movie-card">
                <img src="{movie['poster']}" style="width:100%; aspect-ratio:2/3; object-fit:cover;">
                <div class="movie-info">
                    <div class="movie-title">{movie['title']}</div>
                    <div class="movie-meta">
                        <span class="rating">⭐ {formatted_rating}</span>
                        <span>📅 {year}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def main():
    # Initialize session state
    if 'selected_movie' not in st.session_state:
        st.session_state.selected_movie = None
    if 'search_query' not in st.session_state:
        st.session_state.search_query = ""
    if 'show_search_results' not in st.session_state:
        st.session_state.show_search_results = False

    # Load data
    movies, similarity = load_data()
    movies_list = movies['title'].values

    # Navigation bar (removed login)
    st.markdown("""
    <div class="nav-container">
        <div class="main-header">
            <span style="margin-right:10px;">🎬</span> CineMatch
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- REPLACE HTML SEARCH BAR WITH STREAMLIT TEXT INPUT ---
    search_query = st.text_input(
        "Search for movies...",
        value=st.session_state.get('search_query', ''),
        key="search_query",
        placeholder="Search for movies...",
        label_visibility="collapsed"
    )

    # Handle search results
    if search_query and search_query.strip():
        search_results = search_movies_with_details(search_query, movies)
        if search_results:
            st.session_state.show_search_results = True
            display_search_results(search_results)
        else:
            st.warning(f"No movies found for '{search_query}'. Try a different search term.")
            st.session_state.show_search_results = False
    else:
        if not st.session_state.show_search_results:
            st.session_state.show_search_results = False
    
    # Show homepage content when not displaying search results
    if not st.session_state.show_search_results:
        # Show featured movie carousel
        display_featured_movies_carousel()
        
        # Show trending movies
        display_trending_movies(movies)
        
        # Show genre-based sections
        display_genre_sections()
    
    # Main recommendation interface (always visible)
    st.markdown('<div class="section-title">Get Personalized Recommendations</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Use the selected movie from search/trending or let user select from dropdown
        if st.session_state.selected_movie and st.session_state.selected_movie in movies_list:
            selected_movie = st.selectbox(
                "Choose a movie you enjoyed:",
                movies_list,
                index=list(movies_list).index(st.session_state.selected_movie)
            )
        else:
            selected_movie = st.selectbox(
                "Choose a movie you enjoyed:",
                movies_list
            )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Add spacing
        recommend_button = st.button("Get Recommendations", use_container_width=True)
    
    # Display recommendations
    if recommend_button and selected_movie:
        with st.spinner("Finding perfect matches for you..."):
            movie_names, movie_posters, movie_details = recommend(selected_movie, movies, similarity)
        
        if movie_names:
            st.markdown(f"""
            <div class="recommendation-result">
                <h3>Movies similar to "{selected_movie}"</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Display recommendations in a grid
            cols = st.columns(5)
            
            for i, (name, poster, details) in enumerate(zip(movie_names, movie_posters, movie_details)):
                with cols[i]:
                    # Format the rating
                    formatted_rating = format_rating(details.get('vote_average'))
                    
                    st.markdown(f"""
                    <div class="movie-card">
                        <img src="{poster}" style="width:100%; aspect-ratio:2/3; object-fit:cover;">
                        <div class="movie-info">
                            <div class="movie-title">{name}</div>
                            <div class="movie-meta">
                                <span class="rating">⭐ {formatted_rating}</span>
                                <span>📅 {details.get('release_date', '')[:4] if details.get('release_date') else 'N/A'}</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.error("Sorry, couldn't generate recommendations. Please try another movie.")
    
    # Footer
    st.markdown("""
    <div style="text-align:center; margin-top:3rem; padding:1rem; border-top:1px solid rgba(255,255,255,0.1);">
        <p>© 2025 CineMatch | Powered by TMDB</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
