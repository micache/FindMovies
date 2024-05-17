import tensorflow_datasets as tfds
import pandas as pd

def load_data():
    # load the MovieLens 100k dataset
    movies = tfds.load('movielens/100k-movies', split='train')
    # convert TensorFlow datasets to pandas 
    # ratings_df = tfds.as_dataframe(ratings)
    movies_df = tfds.as_dataframe(movies)
    return [], movies_df