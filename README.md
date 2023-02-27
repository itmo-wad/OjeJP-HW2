Here is my submission for homework 2


The following was implemented:

Basic part: Implement authentication feature
    1) Listen on localhost:5000
    2) Render authentication form at http://localhost:5001/ (5000 wasn't possible because it seems to be in use on my system)
    3) Redirect user to profile page if successfully authenticated
    4) Show profile page for authenticated user only at http://localhost:5001/profile
    5) User name and password are stored in Mongodb
 
 Advanced part:
    1) Implement feature that allows users to create new account, profile will be shown with data respected to each account.
    2) Implement password hashing, logout and password change features
    3) Allow users to update profile picture (new user will have a default profile picture)
    4) Allow users to update profile information
 
 
 Challenging part:
    1)Implement notification, an active user will receive notification when a new account is created. (Not implemented)


Prerequisites
    1) Running MongoDB on localhost:27017
    2) Install docker
            docker pull mongodb (pull mongodb image to local system)
             docker run --name mongodb -d -p 27023:27017 mongo (start container)
    3) Install docker-compass (GUI for mongodb)
            Initialize connection with mongodb://localhost:27023

requirements.txt
