# MoviesDB
#### Video Demo:  <https://youtu.be/p2tixlagaXc>

<img src="static/media/web-project-front-page.png">

## Contents
- [Description](#description)
- [Folders](#folders)
- [Resources](#resources)
- [Contact](#contact)

## Description
This is the final project for CS50 x 2024 made by <a href="https://www.github.com/hunxio/">hunxio</a>.
This website is hosted locally.
MoviesDB wants to create a website, called MoviesDB, where people can sign up an account
and get access to the daily top trending movies and not only; it will also give the user the opportunity to create
its own personal collection of movies, or manage its account in case they need to modify their data.
I gave myself a month to get as much done for this project, even though some of the ideas and parts are missing (you can check the planning in planning/plan.drawio),
I am quite happy about the results. *Quack!*
The application has a mainpage which changes depending if an user is currently logged in or not, which defines if there is a session active or not. If no users are logged in
the homepage will show a small title and motto, and in the navbar you will be able to access the "Sign Up" or "Log In" page by clicking on the buttons. While you register an
account you will be asked for some personal informations, if any of those informations do not satisfy the requirements to make an account "able" to be created, you will see
an error page, showing you what is the problem encountered during the registration; if everything is fine you will see a page with a link redirecting you to the "Log In" page.
The data will be stored in a database and, the password is hashed and salted, and when you try to log in app.py will go through a series of checks to see if everything is right
(and if the account exist of course!). Once you are logged in, the homepage will be slightly different, showing you three big sections:
- <b>Collection :</b> here you will be able to access your movie's collection, if you have added any to it. It will be displayed like a list containing the poster and title of the movie (informations are retrieved through the API);
- <b>Gallery :</b> you can access the application movie database (informations are retrieved through the API), it will show everyday the top trending movies, you can also search for a movie by tipying the title in the search bar;
- <b>Personal Data :</b> this section is your typical "Settings" page, here you will be able to change your password and username. The password has a pattern that needs to be followed, same for the username but less restrictive it will be checked also if the username you are trying to choose already exists in the database or not.
<br>
I have mostly used Bootstrap for the FrontEnd part of this project, modified the layout and parts in both CSS and HTML.
<br>

## Folders
- <b>planning :</b> You can see what was the idea for this project, you can run it on VSCode with an extension called "Draw.io Integration" by Henning Dieterichs;
- <b>static :</b> This folder contains the CSS file and a folder called "media", where you can find all the media I used for this project;
- <b>templates :</b> Every HTML page is contained here, they are all based on the layout.html page, and every other page is an extension of it;
- <b>.gitignore :</b> It contains file that I have decided to not upload, they really do not contain anything special, just for good practice to learn to use it and understand why it is important;
- <b>README.md :</b> This file, which contains a brief explanation and documentation about this project;
- <b>app.py :</b> The main file, it contains the the code that I wrote to initialize the application;
- <b>requirements.txt :</b> I used this file to fast install all the lib I needed to run the project (since I worked on my laptop mainly but sometimes on my Computer too);
- <b>utils.py :</b> It is a collection of personal defs that I made to use in app.py.

  
## Resources

<b>CS50x2024 Course:</b>
https://www.edx.org/

<b>Bootstrap for front-end resources:</b>
https://getbootstrap.com/

<b>API Service provided by:</b>
https://www.themoviedb.org/

<b>Flask Documentation:</b>
https://flask.palletsprojects.com/en/3.0.x/

<b> Flask installation and Virtual Enviroment Set up:</b>
https://phoenixnap.com/kb/install-flask

<b>Python, HTML, CSS Resources:</b>
https://www.w3schools.com/

## Contact

For more informations about this project, visit my github profile 

[![My Skills](https://skillicons.dev/icons?i=github)](https://github.com/hunxio)
