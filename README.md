# Movie Recommender

## Index

* [1. Introduction](#1-introduction)
* [2. Structures](#2-structure)
* [3. Installation](#3-installation)
* [4. Usage](#4-usage)
* [5. References](#5-references)

## 1. Introduction

Tired of scrolling endlessly to find the perfect movie? Our app is here to help! Get personalized movie recommendations based on your tastes and preferences.

Features:
- Personalized Suggestions: Discover movies tailored to your viewing habits.
- Huge Movie Library: Find movies from all genres, all the classic included.
- User Reviews: You can choose a number (on a scale from 1 to 5) to express your rating to movies you have seen.
- Watchlist: Keep track of movies you want to watch.

## 2. Structure

The directory structure should look like this:

* `app.py` : This script runs the main code contains UI and other interaction
* `model.py` : This file contains function to train, evaluate and predict from a model
* `ModelClass.py` : This file contains 2 classes(models) popular in recommendation system (Retrievial Model and Multitask Model)
* `genres_occu_list` : This file stores list of genres and occupation.
* `multitask_model.ipynb` and `retrieval_model.ipynb` : These are jupyterlab file for building model
* `requirements.txt` : Necessary Dependecies
* `tests/` : is the folder contains script for automated test

## 3. Installation

### Requirements
To use Trivix, you must have the following installed
- python >= 3.11.9
- streamlit
- tensorflow
- pandas
- requests

### Getting Started
1. Clone the repository from GitHub:
```bash
$ git clone https://github.com/micache/FindMovies.git
```
2. Install virtual environment (conda) (recommended):
- You need to install anaconda (or miniconda): https://www.anaconda.com/download
- Then open the anaconda prompt (or anaconda.navigator) to create new environment:
```bash
$ conda create --name <env-name> --file </path/to/requirements.txt>
```
3. Activate virtual environment (recommended):
* Using anaconda prompt (cmd)
```cmd
> conda activate <env-name>
```
4. Select the interpreter for your python file to run
* If you are using Visual Studio Code, you can choose it in the right-down corner of the screen
* For the other you should search for choosing interpreter for that IDE / code editing application

## 4. Usage

This application is built with a website-like interface, very user-friendly.
You have to provide some personal information before get to the home page. Your personal information is only for caculating and helping the model to predict more percisely.

Here are examples of how to run the code. In Terminal, run:

```bash
$ streamlit run app.py
```
A website will be hosted on the port 8501. For specific, it will be hosted in your web browser at `http://localhost:8501`

## 5. References
- https://www.tensorflow.org/recommenders/examples/quickstart
- https://docs.streamlit.io/
- https://conda.io/projects/conda/en/latest/user-guide/getting-started.html

