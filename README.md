# MovieService


## Description

movie information service that allows you to register, log in, view saved public and private movies, and create and modify private movies.

## How to run it?

first install [Python](https://www.python.org/), then create a virtual enviroment using the comand:

```
python -m venv venv
```

then isntall packages using the comand:

```
pip install -r requirements.txt
```

then you should be able to run the service using the comand.

```
python manage.py runserver
```

## Calling the endpoints

### Registration

This service will let you create a user unisg a email and a password, it use a}the post method, is called using the link http://127.0.0.1:8000/registration/ and you have to send a json like this:
```json
{
    "email": "test@email.com",
    "password": "password you choose"
}
```

### Login

This service let you log in and get a jwt token, it use a post method, is called using the link http://127.0.0.1:8000/login/ and you have to send a json like this:

```json
{
    "email": "test@email.com",
    "password": "password you choose"
}
```

if the user is already registered you would get a response linke this:

```json
{
    "jwt": "JWT Token"
}
```

### Get Public list 

this service will let a user read all the movies that are public, it use the get method and is called using the link http://127.0.0.1:8000/getPublicMovies/,
you have to send the jwt token in the headers of the request in the key "Token". You shoud get a json response like this one:

```json
{
    "movies": [list of public movies]
}
```

### Get Private list 

This service will let a user read all the movies that are private of the user, it use the get method and is called using the link http://127.0.0.1:8000/getPrivateMovies/,
you have to send the jwt token in the headers of the request in the key "Token". You shoud get a json response like this one:

```json
{
    "movies": [list of private movies]
}
```

### Add a private movie

This service will let a logged user create a private movie, this service use the method post and is called using the link http://127.0.0.1:8000/addItem/, it requires  the jwt token in the headers of the request in the key "Token" and a json similar to disone in the body:

```json
{
    "name":" Name of the movie",
    "gender":"Gender of the movie",
    "duration":"Duratin un minutes",
    "objectType":"private",
    "clasification":"Clasification of the movie"
}
```

### Edit a private movie

This service let a logged user edit one of the private movies previously created by him, this service use the method post and is called using the link http://127.0.0.1:8000/addItem/, it requires  the jwt token in the headers of the request in the key "Token" and a json similar to disone in the body:

```json
{
    "id":"Id of the movie",
    "name":" Name of the movie",
    "gender":"Gender of the movie",
    "duration":"Duratin un minutes",
    "clasification":"Clasification of the movie"
}
```

