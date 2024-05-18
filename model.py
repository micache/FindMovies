import tensorflow_datasets as tfds
import tensorflow_recommenders as tfrs
import pandas as pd
from genres_occu_list import occu_list
import time
import tensorflow as tf
import streamlit as st
import numpy as np
from ModelClass import MovieModel

def load_data():
    # load the MovieLens 100k dataset
    movies = tfds.load('movielens/100k-movies', split='train')
    # convert TensorFlow datasets to pandas 
    # ratings_df = tfds.as_dataframe(ratings)
    movies_df = tfds.as_dataframe(movies)
    return [], movies_df

def convert_gender(gender):
    if gender == "Male":
        return True
    else:
        return False

def convert_occu(occu):
    for i, sub in enumerate(occu_list):
        if occu in sub:
            return np.int64(i)

def process_data():
    # movies data
    movies = tfds.load("movielens/100k-movies", split="train")
    # ratings data
    ratings = tfds.load("movielens/100k-ratings", split="train")

    ratings = ratings.map(lambda x: {
        "movie_title": x["movie_title"],
        "user_id": x["user_id"]
    })
    movies = movies.map(lambda x: x["movie_title"])

    return movies, ratings

# sort ratings data by time
def sort_ratings(ds):
    timestamps = []
    features_list = []

    for example in ds:
        timestamps.append(example['timestamp'])
        features_list.append(example)

    # convert list to tensor
    timestamps = tf.convert_to_tensor(timestamps)
    features_list = tf.stack(features_list)
    # sort index
    sorted_indices = tf.argsort(timestamps)
    # sort all data
    sorted_features = tf.gather(ds, sorted_indices)
    return tf.data.Dataset.from_tensor_slices(sorted_features)

def create_and_train_model(movies, ratings):
    # batch data and unique
    movie_titles = movies.batch(2_000)
    user_ids = ratings.batch(1_000_000).map(lambda x: x["user_id"])    
    unique_movie_titles = np.unique(list(movie_titles))
    unique_user_ids = np.unique(list(user_ids))

    # create model
    embedding_dimension = 32

    user_model = tf.keras.Sequential([
        tf.keras.layers.StringLookup(
            vocabulary=unique_user_ids, mask_token=None),
            tf.keras.layers.Embedding(len(unique_user_ids) + 1, embedding_dimension)
    ])

    movie_model = tf.keras.Sequential([
    tf.keras.layers.StringLookup(
        vocabulary=unique_movie_titles, mask_token=None),
        tf.keras.layers.Embedding(len(unique_movie_titles) + 1, embedding_dimension)
    ])

    # metrics
    metrics = tfrs.metrics.FactorizedTopK(
        candidates=movies.batch(128).map(movie_model)   
    )

    # task
    task = tfrs.tasks.Retrieval(
        metrics=metrics
    )

    # create instance and compile
    model = MovieModel(user_model, movie_model, task)
    model.compile(optimizer=tf.keras.optimizers.Adagrad(learning_rate=0.1))
    # fit
    model.fit(ratings.shuffle(100_000).batch(8192), epochs=5)
    return model

def query(model, movies):
    # create a model that takes in raw query features, and
    index = tfrs.layers.factorized_top_k.BruteForce(model.user_model)
    # recommends movies out of the entire movies dataset.
    index.index_from_dataset(
        movies.batch(128).map(lambda title: (title, model.movie_model(title)))
    )

    return index

def predict(user, list_of_rate):

    if 'movies_are_found' not in st.session_state:
        # process data for training
        movies, ratings = process_data()

        # add new row
        for x in list_of_rate:
            # create new row
            row = {
                'movie_title': [x['movie_title']],
                'user_id': ['7000']
            }
            # append to ratings dataset
            row = tf.data.Dataset.from_tensor_slices(row)
            ratings = ratings.concatenate(row)
        
        model = create_and_train_model(movies, ratings)
        # query
        index = query(model, movies)
        # get recommendations.
        _, titles = index(np.array(["7000"]), k=10)
        st.session_state.movies_are_found = titles
    
    # return list of movie name
    return [s.numpy().decode('utf-8') for s in st.session_state.movies_are_found[0]]

