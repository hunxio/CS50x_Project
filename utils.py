import os

import sqlite3
import argon2
import requests
from dotenv import load_dotenv
from urllib.parse import quote
from flask import Flask, render_template, redirect, request, session

load_dotenv()
api_key = os.getenv("API_KEY")


# It will close the database connection and return an error page #
def ErrorConnection(con, code_error):
    con.close()
    return render_template("errorpage.html", message=code_error)


# Basic template for error page, in case no access to the database and user did not login #
def ErrorTemplate(code_error):
    return render_template("errorpage.html", message=code_error)


# Access to database and looks for user's username by filtering by email (session host)
def acquireSessionUsername(cur):
    email = session.get("email")
    usernameCur = cur.execute("SELECT username FROM users WHERE email = ?;", (email,))
    userUsername = usernameCur.fetchone()[0]
    return userUsername


def acquireSessionId(cur):
    email = session.get("email")
    idCur = cur.execute("SELECT id FROM users WHERE email = ?;", (email,))
    userId = idCur.fetchone()[0]
    return userId


def hashPassword(password):
    # Password hash and salt with argon2 #
    hasher = argon2.PasswordHasher()
    hashPassword = hasher.hash(password)
    return hashPassword


# API SERVICE PROVIDED BY https://www.themoviedb.org/ #
def trendingMovieAPI(position):

    url = "https://api.themoviedb.org/3/trending/movie/day?language=en-US"

    headers = {"accept": "application/json", "Authorization": "Bearer " + str(api_key)}

    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        movie_data = data["results"][
            position
        ]  # Accessing the first movie object in the results list
        title = movie_data["title"]
        image = movie_data["backdrop_path"]
        # Base URL
        base_image_url = "https://image.tmdb.org/t/p/w500"
        # Relative to movie URL
        poster_path = str(image)

        # Complete URL for Movie Image
        complete_image = base_image_url + poster_path

        overview = movie_data["overview"]
        release_date = movie_data["release_date"]
        vote_average = movie_data["vote_average"]
        movie_id = movie_data["id"]
        return title, complete_image, overview, release_date, vote_average, movie_id
    else:
        return ErrorTemplate("Failed to retrieve data. API not working properly.")


def searchAPI(position, query):
    url = "https://api.themoviedb.org/3/search/movie"

    headers = {"accept": "application/json", "Authorization": "Bearer " + str(api_key)}

    # Encode the query parameter properly
    encoded_query = quote(query)

    params = {"query": encoded_query}  # Add the encoded query parameter

    response = requests.get(url, headers=headers, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # Check if results are not empty
        if "results" in data and data["results"]:
            # Check if the specified position is within the bounds of the results list
            if 0 <= position < len(data["results"]):
                # Accessing the movie object at specified position
                movie_data = data["results"][position]
                title = movie_data["title"]
                image = movie_data["backdrop_path"]
                # Base URL
                base_image_url = "https://image.tmdb.org/t/p/w500"
                # Relative to movie URL
                poster_path = str(image)

                # Complete URL for Movie Image
                complete_image = base_image_url + poster_path

                overview = movie_data["overview"]
                release_date = movie_data["release_date"]
                vote_average = movie_data["vote_average"]
                movie_id = movie_data["id"]
                return (
                    title,
                    complete_image,
                    overview,
                    release_date,
                    vote_average,
                    movie_id,
                )
            else:
                return None
        else:
            return None
    else:
        return "Failed to retrieve data. API not working properly."


def idSearchAPI(movieId):

    url = "https://api.themoviedb.org/3/movie/" + str(movieId)

    headers = {"accept": "application/json", "Authorization": "Bearer " + str(api_key)}

    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        title = response.json()["title"]
        image = response.json()["poster_path"]
        # Base URL
        base_image_url = "https://image.tmdb.org/t/p/w500"
        # Relative to movie URL
        poster_path = str(image)

        # Complete URL for Movie Image
        complete_image = base_image_url + poster_path

        return title, complete_image
    else:
        return ErrorTemplate("Failed to retrieve data. API not working properly.")
