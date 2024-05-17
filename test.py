import streamlit as st
import pandas as pd

# Simulated dataset with multiple genres per movie
data = {
    "Movie Name": ["Inception", "The Matrix", "Interstellar", "The Godfather", "Skyfall"],
    "Genres": [
        ["Sci-Fi", "Adventure"],  # Multiple genres for Inception
        ["Sci-Fi", "Action"],     # Multiple genres for The Matrix
        ["Sci-Fi", "Drama"],      # Multiple genres for Interstellar
        ["Crime", "Drama"],       # Multiple genres for The Godfather
        ["Action", "Thriller"]    # Multiple genres for Skyfall
    ]
}
movies_df = pd.DataFrame(data)

def main():
    st.title("Movie Search App")

    # User inputs
    movie_name_query = st.text_input("Enter movie name:")

    # Generate checkboxes for each unique genre dynamically
    all_genres = set(genre for sublist in movies_df['Genres'] for genre in sublist)
    selected_genres = []
    genre_cols = st.columns(4)  # Organizing checkboxes into rows of four columns
    for index, genre in enumerate(all_genres):
        with genre_cols[index % 4]:
            if st.checkbox(genre, key=genre):
                selected_genres.append(genre)

    # Search button
    if st.button("Search"):
        # Filter by name if specified
        if movie_name_query:
            result = movies_df[movies_df["Movie Name"].str.contains(movie_name_query, case=False)]
        else:
            result = movies_df

        # Further filter by selected genres if any
        if selected_genres:
            # Use a lambda to check if any selected genre is in a movie's genres
            result = result[result['Genres'].apply(lambda genres: any(g in selected_genres for g in genres))]

        # Display results
        if not result.empty:
            st.write("## Search Results")
            st.dataframe(result)
        else:
            st.write("No results found.")

if __name__ == "__main__":
    main()
