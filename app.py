import streamlit as st
import pandas as pd
import numpy as np
from model import load_data, predict
from genres_occu_list import convert_genres, occu_list
import requests
import time

# page control
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# navigate
def navigate_to_page1():
    del st.session_state.movies_are_found 
    st.session_state.page = 'home'

# navigate
def navigate_to_page2():
    st.session_state.page = 'page2'

# save user regis info
def save_user_data(data):
    # save user data in session state
    st.session_state.user_data = data
    

# regis form
def show_registration_form():
    # show the registration form and handle data submission.
    with st.form(key='registration_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        gender = st.selectbox("Gender", options=["Male", "Female"])
        occupation = st.selectbox("Occupation", options=occu_list)
        age = st.number_input("Age", min_value=18, max_value=100, step=1, format='%d')

        if st.form_submit_button("Register"):
            user_data = {
                'username': username,
                'password': password,  
                'gender': gender,
                'occupation' : occupation,
                'age': age
            }
            save_user_data(user_data)
            st.success(f"User {username} registered successfully! Click again to go home page")

# just convert to dataframe 1 time
if 'ratings_df' not in st.session_state:
    st.session_state.ratings_df, st.session_state.movies_df = load_data()
    # convert title to str
    st.session_state.movies_df['movie_title'] = st.session_state.movies_df['movie_title'].str.decode('utf-8')

# fetch the short plot from OMDb
def get_movie_plot(title, api_key):
    if title == 'unknown':
        return "Plot not found"
    
    index = title.find('(')
    year = title[index:]
    title = title[:index]

    year = title[1:-1]

    # build the API URL
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}&y={year}&plot=full"
    # make request
    response = requests.get(url)
    # convert the response to JSON
    movie_data = response.json()
    # check if the response contains a movie plot
    if 'Plot' in movie_data:
        return movie_data['Plot']
    else:
        return "Plot not found"

# display details of a movie.
def show_movie_details(movie_id, movie_title, movie_genres):
    st.write(f"### {movie_title}")
    st.write(f"### ID: {movie_id}")
    st.write("Genres:", ', '.join([convert_genres[genre] for genre in movie_genres]))
    # get api key
    with open('D:/project/toolkit/apikey.txt', 'r') as file:
        api_key = file.read()
    st.write(f"Plot: {get_movie_plot(movie_title, api_key)}")

def show_movie(row, create_slider_or_not):
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
        st.session_state['_' + key + '_movie_id'] = movie_id
        st.session_state['_' + key + '_movie_title'] = movie_title
        st.session_state['_' + key + '_movie_genres'] = movie_genres
        
    if (create_slider_or_not):
        # Create a slider for scoring each movie
        score = st.slider("Score", 
                        min_value=0, 
                        max_value=5, 
                        key=key,
                        value=st.session_state['_' + key])
        st.session_state['_' + key] = score

def main_page():
    st.title(f"Hello, {st.session_state.user_data['username']}!")
    st.title('Looking for a new movie ?')
    st.markdown("##### Please rate some of your watched movie below to help us find some movies best fit with you:")
    movies_df = st.session_state.movies_df

    # query step
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
    for index, row in result[:20].iterrows():
        show_movie(row, True)

    st.button("Finish", on_click=navigate_to_page2)

# train model and predict
def page2():
    min_movie_id = 1
    max_movie_id = 3952
    score_list = []
    # get all the movies have been rated
    for i in range(1, max_movie_id + 1):
        key = f"_score_{i}"
        if key in st.session_state and st.session_state[key] > 0:
            score = {
                'rate': float(st.session_state[key]),
                'movie_id': st.session_state[key + '_movie_id'],
                'movie_title': st.session_state[key + '_movie_title'],
                'movie_genres': st.session_state[key + '_movie_genres']
            }
            score_list.append(score)

    recom_movie = predict(st.session_state.user_data, score_list)
    
    st.title('Result')
    st.write("### There are some movies you may like: ")
    for index, row in st.session_state.movies_df.iterrows():
        if (row['movie_title'] in recom_movie):
            show_movie(row, False)
    
    st.write('### Not happy with the list? Try again!')
    st.button("Go back to home page", on_click=navigate_to_page1)

def main():

    # navigation control based on session state
    if 'user_data' not in st.session_state:
        show_registration_form()
    elif st.session_state.page == 'home':
        main_page()
    elif st.session_state.page == 'page2':
        page2()

if __name__ == "__main__":
    main()