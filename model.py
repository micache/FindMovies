import tensorflow_datasets as tfds
import pandas as pd

def load_data():
    # load the MovieLens 100k dataset
    ratings, movies = tfds.load('movielens/100k-ratings', split='train'), tfds.load('movielens/100k-movies', split='train')
    # convert TensorFlow datasets to pandas 
    ratings_df = tfds.as_dataframe(ratings)
    movies_df = tfds.as_dataframe(movies)
    return ratings_df, movies_df