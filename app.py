import streamlit as st
import pandas as pd
import numpy as np
from model import load_data

convert_genres = [ 'Action'
	,' Adventure'
	,' Animation'
	,' Children'
	,' Comedy'
	,' Crime'
	,' Documentary'
	,' Drama'
	,' Fantasy'
	,' Film-Noir'
	,' Horror'
	,' Musical'
	,' Mystery'
	,' Romance'
	,' Sci-Fi'
	,' Thriller'
	,' War'
	,' Western'
    ,' Sport'
    ,' Unknown'
]

# page control
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def navigate_to_page1():
    st.session_state.page = 'home'

def navigate_to_page2():
    st.session_state.page = 'page2'

def show_movie_details(movie_id, movie_title, movie_genres):
    """Display details of a movie."""
    st.write(f"### {movie_title}")
    st.write("Genres:", ', '.join([convert_genres[genre] for genre in movie_genres]))

# just convert to dataframe 1 time
if 'ratings_df' not in st.session_state:
    st.session_state.ratings_df, st.session_state.movies_df = load_data()
    # convert title to str
    st.session_state.movies_df['movie_title'] = st.session_state.movies_df['movie_title'].str.decode('utf-8')

def show_movie(row):
    movie_id = row['movie_id'].decode('utf-8')
    movie_title = row['movie_title']
    movie_genres = row['movie_genres']

    # Create a button for each movie
    if st.button(movie_title):
        show_movie_details(movie_id, movie_title, movie_genres)

    key = f"score_{movie_id}"

    # create dummy (_key) to save the current score
    if ('_' + key) not in st.session_state:
        st.session_state['_' + key] = 0

    # Create a slider for scoring each movie
    score = st.slider("Score", 
                      min_value=0, 
                      max_value=10, 
                      key=key,
                      value=st.session_state['_' + key])
    st.session_state['_' + key] = score

def main_page():
    st.title('Movie recommendation')
    movies_df = st.session_state.movies_df

    movie_name_query = st.text_input("Enter movie name:")

    # Generate checkboxes for each unique genre dynamically
    all_genres = set(genre for sublist in movies_df['movie_genres'] for genre in sublist)
    
    selected_genres = []
    # checkboxes into rows of four columns
    genre_cols = st.columns(4)  
    for index, genre in enumerate(all_genres):
        with genre_cols[index % 4]:
            if st.checkbox(convert_genres[genre], key=genre):
                selected_genres.append(genre)

    result = movies_df
    # Filter by name if specified
    if movie_name_query:
        result = movies_df[movies_df["movie_title"].str.contains(movie_name_query, case=False)]

    # Further filter by selected genres if any
    if selected_genres:
        # Use a lambda to check if any selected genre is in a movie's genres
        result = result[result['movie_genres'].apply(lambda genres: set(selected_genres).issubset(set(genres)))]
    # print out movie
    st.markdown("## Featured movies")
    for index, row in result[:50].iterrows():
        show_movie(row)

    st.button("Finish", on_click=navigate_to_page2)

def page2():
    st.title('Page 2')
    st.write("You are now on page 2. This page is only accessible via a button from the main page.")
    st.button("Go to Page 1", on_click=navigate_to_page1)

def main():
    # navigation control based on session state
    if st.session_state.page == 'home':
        main_page()
    elif st.session_state.page == 'page2':
        page2()

if __name__ == "__main__":
    main()