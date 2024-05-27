# Movie Recommender

## Index

* [1. Introduction](#1-introduction)
* [2. Techical Overview](#2-technical-overview)
* [3. Structures](#3-structure)
* [4. Installation](#4-installation)
* [5. Usage](#5-usage)
* [6. Packaging to Docker](#6-packaging-to-docker)
* [7. References](#7-references)

## 1. Introduction

Tired of scrolling endlessly to find the perfect movie? Our app is here to help! Get personalized movie recommendations based on your tastes and preferences.

Features:
- Personalized Suggestions: Discover approximately 1700 movies tailored to your viewing habits.
- Huge Movie Library: Find movies from all genres, all the classic included.
- User Reviews: You can choose a number (on a scale from 1 to 5) to express your rating to movies you have seen.
- Watchlist: Keep track of movies you want to watch.

## 2. Technical Overview
* This application gains your personal information, and your rating on movies which you rated on the home page. After that, it will append your data into a dataset which is loaded earlier and push the final dataset to train a model with parameter is setup before. Finally, it will predict the top 10 movies are suitable with you.
* The model in this application is Multitask Model, which is combine of Retrieval Model (try to predict the top-k movies you may like) and a MLP model to predict rating for each movies. The model is programmed based on **tensorflow** library
* The UI is create by using the **Streamlit** components, and the detail of the movie is gotten by calling the API to the OMDb database.
* There is a `test/` folder contains all the script to automated testing (using **pytest**)

## 3. Structure

The directory structure should look like this:

* `app.py` : This script runs the main code contains UI and other interaction
* `model.py` : This file contains function to train, evaluate and predict from a model
* `ModelClass.py` : This file contains 2 classes(models) popular in recommendation system (Retrievial Model and Multitask Model)
* `genres_occu_list` : This file stores list of genres and occupation.
* `multitask_model.ipynb` and `retrieval_model.ipynb` : These are jupyterlab file for building model
* `requirements.txt` : Necessary Dependecies
* `tests/` : is the folder contains script for automated test

## 4. Installation

### Requirements
To use this app, you must have the following installed
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
<<<<<<< HEAD
$ conda create -n <env-name> -f </path/to/environment.yml>
=======
$ conda create -n <env-name> -f </path/to/requirements_conda.txt>
>>>>>>> 837b7f40104b5e85b1b259e45fb152f4dea3da29
```
* If you are not using virtual environment, you can run this command for install neccessary dependencies:
```cmd
> pip install -r requirements.txt
```
3. Activate virtual environment (recommended):
* Using anaconda prompt (cmd)
```cmd
> conda activate <env-name>
```
4. Getting API key for the OMDb database:
* Go to this website: https://www.omdbapi.com/apikey.aspx and type in your email to get the API key
* After retrieve the API key, create a file name `apikey.txt` and put your key in here
5. Select the interpreter for your python file to run
* If you are using Visual Studio Code, you can choose it in the right-down corner of the screen
* For the other you should search for choosing interpreter for that IDE / code editing application

## 5. Usage

This application is built with a website-like interface, very user-friendly.
You have to provide some personal information before get to the home page. Your personal information is only for caculating and helping the model to predict more percisely.

Here are examples of how to run the code. In Terminal, run:

```bash
$ streamlit run app.py
```
A website will be hosted on the port 8501. For specific, it will be hosted in your web browser at `http://localhost:8501`

## 6. Packaging to Docker
If you want to package your application into a Docker image and run it in a containerized environment, follow these steps:
*  Navigate to the directory containing the Dockerfile and run the following command to build the Docker image:
```cmd
> docker build -t <app_name>
```
* Run the Docker image:
```cmd
> docker run -p <app_name>
```
The application will be hosted on port 8501.

## 7. References
- https://www.tensorflow.org/recommenders/examples/quickstart
- https://docs.streamlit.io/
- https://conda.io/projects/conda/en/latest/user-guide/getting-started.html

