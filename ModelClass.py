import tensorflow_recommenders as tfrs
import tensorflow as tf

from typing import Dict, Text

class RetrievalModel(tfrs.Model):

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

# combine between retrieval and ratings model
class MultitaskModel(tfrs.models.Model):

  def __init__(self, user_model, movie_model, rating_weight, retrieval_weight, task) -> None:
    super().__init__()

    embedding_dimension = 32
    self.user_model: tf.keras.Model = user_model
    self.movie_model: tf.keras.Model = movie_model
    # MLP model for predict rating
    self.rating_model = tf.keras.Sequential([
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dense(1),
    ])

    # ratings tasks.
    self.rating_task: tf.keras.layers.Layer = tfrs.tasks.Ranking(
        loss=tf.keras.losses.MeanSquaredError(),
        metrics=[tf.keras.metrics.RootMeanSquaredError()],
    )

    # retrieval task
    self.retrieval_task: tf.keras.layers.Layer = task
    # loss weights.
    self.rating_weight = rating_weight
    self.retrieval_weight = retrieval_weight

  def call(self, features: Dict[Text, tf.Tensor]):
    # pick out features and pass them into the models.
    user_embeddings = self.user_model(features["user_id"])
    movie_embeddings = self.movie_model(features["movie_title"])

    return (
        user_embeddings,
        movie_embeddings,
        # apply the multi-layered rating model to a concatentation of
        # user and movie embeddings.
        self.rating_model(
            tf.concat([user_embeddings, movie_embeddings], axis=1)
        ),
    )

  def compute_loss(self, features: Dict[Text, tf.Tensor], training=False):

    ratings = features.pop("user_rating")

    user_embeddings, movie_embeddings, rating_predictions = self(features)

    # compute the loss for each task.
    rating_loss = self.rating_task(
        labels=ratings,
        predictions=rating_predictions,
    )
    retrieval_loss = self.retrieval_task(user_embeddings, movie_embeddings)

    # combine them using the loss weights.
    return (self.rating_weight * rating_loss
            + self.retrieval_weight * retrieval_loss)