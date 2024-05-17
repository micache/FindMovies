import streamlit as st
import tensorflow_datasets as tfds

def load_data():
    # Load the MovieLens 100k dataset
    ratings, movies = tfds.load('movielens/100k-ratings', split='train'), tfds.load('movielens/100k-movies', split='train')
    # Convert TensorFlow datasets to pandas DataFrames for easier manipulation
    movies_df = tfds.as_dataframe(movies)
    movies_df['movie_title'] = movies_df['movie_title'].str.decode('utf-8')  # Decode byte strings
    return movies_df

def show_movie_details(movie_id, movie_title, movie_genres):
    """Display details of a movie."""
    st.write(f"### {movie_title}")
    st.write("Genres:", ', '.join([genre.decode('utf-8') for genre in movie_genres]))

@st.cache(allow_output_mutation=True)
def get_movie_scores():
    return {}

def main():
    st.title("MovieLens Viewer")

    movies_df = load_data()
    movie_scores = get_movie_scores()

    for _, row in movies_df.iterrows():
        movie_id = row['movie_id']
        movie_title = row['movie_title']
        movie_genres = row['movie_genres']

        # Create a button for each movie
        if st.button(movie_title):
            show_movie_details(movie_id, movie_title, movie_genres)

        # Create a slider for scoring each movie
        score = st.slider("Score", 0, 5, key=f"score_{movie_id}")
        movie_scores[movie_id] = score

    if st.button("Submit Scores"):
        st.write("Submitted scores:")
        for movie_id, score in movie_scores.items():
            movie_title = movies_df.loc[movies_df['movie_id'] == movie_id, 'movie_title'].iloc[0]
            st.write(f"{movie_title}: {score}")

if __name__ == "__main__":
    main()
