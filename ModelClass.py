import tensorflow_recommenders as tfrs
import tensorflow as tf

from typing import Dict, Text

class MovieModel(tfrs.Model):

  def __init__(self, user_model, movie_model, task):
    super().__init__()
    self.movie_model: tf.keras.Model = movie_model
    self.user_model: tf.keras.Model = user_model
    self.task: tf.keras.layers.Layer = task

  def compute_loss(self, features: Dict[Text, tf.Tensor], training=False):
    # pick out the user features and pass them into the user model.
    user_embeddings = self.user_model(features["user_id"])
    # and pick out the movie features and pass them into the movie model,
    # getting embeddings back.
    positive_movie_embeddings = self.movie_model(features["movie_title"])

    # computes the loss and the metrics.
    return self.task(user_embeddings, positive_movie_embeddings)