# A Production Based FastAPI-MongoDB Template
I have used Beanie ODM for MongoDB database model with FastAPI.
<p>
    <a href="https://github.com/MahmudJewel/FastAPI-MongoDB-Template/fork">
        <img src="https://img.shields.io/github/forks/MahmudJewel/FastAPI-MongoDB-Template.svg?style=social&label=Fork" />
    </a>
    <a href="https://github.com/MahmudJewel/FastAPI-MongoDB-Template/fork">
        <img src="https://img.shields.io/github/stars/MahmudJewel/FastAPI-MongoDB-Template.svg?style=social&label=Stars" />
    </a>
    <!-- <a href="https://github.com/MahmudJewel/FastAPI-MongoDB-Template/fork">
        <img src="https://img.shields.io/nuget/dt/Azylee.Core.svg" />
    </a> -->
</p>
<p>
    If the repo is helpful for you, please give a star and fork it.
</p>
<a href="https://github.com/MahmudJewel/FastAPI-MongoDB-Template/fork">
    Click here to download/fork the repository
</a>

## Features:
* FastAPI project structure tree
* user module
    - id, first name, last name, **email** as username, **password**, role, is_active created_at, updated_at 
* RBAC implementation
* authentication => JWT
* middleware
* three types of server
    - production, development, test
* UUID as primary key

## User module's API
| SRL | METHOD | ROUTE | FUNCTIONALITY | Fields | Access | 
| ------- | ------- | ----- | ------------- | ------------- |------------- |
| *1* | *POST* | ```/login``` | _Login user_| _**email**, **password**_| _All User_|
| *2* | *POST* | ```/refresh/?refresh_token=``` | _Refresh access token_| _None_| _All User_|
| *3* | *POST* | ```/users/``` | _Create new user_|_**email**, **password**, first name, last name_| _Anyone_|
| *4* | *GET* | ```/users/``` | _Get all users list_|_email, password, first name, last name, role, is_active, created_at, updated_at, id_|_Admin_|
| *5* | *GET* | ```/users/me/``` | _Get current user details_|_email, password, first name, last name, role, is_active, created_at, updated_at, id_|_Any User_|
| *6* | *GET* | ```/users/{user_id}``` | _Get indivisual users details_|_email, password, first name, last name, role, is_active, created_at, updated_at, id_|_Any User_|
| *7* | *PATCH* | ```/users/{user_id}``` | _Update the user partially_|_email, password, is_active, role_|_Admin_|
| *8* | *DELETE* | ```/users/{user_id}``` | _Delete the user_|_None_|_Admin_|

## Project Structure
```sh
├── app
│   ├── api
│   │   ├── endpoints   # Contains modules for each feature (user, product, payments).
│   │   │   ├── __init__.py
│   │   │   └── user
│   │   │       ├── auth.py
│   │   │       ├── functions.py
│   │   │       ├── __init__.py
│   │   │       └── user.py
│   │   ├── __init__.py
│   │   └── routers     # Contains FastAPI routers, where each router corresponds to a feature.
│   │       ├── api.py
│   │       ├── __init__.py
│   │       └── user.py
│   ├── core    # Contains core functionality like database management, dependencies, etc. 
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── __init__.py
│   ├── main.py     # Initializes the FastAPI app and brings together various components.
│   ├── models      # Contains modules defining database models for users, products, payments, etc.
│   │   ├── common.py
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas    # Pydantic model for data validation
│   │   ├── __init__.py
│   │   └── user.py
│   └── utils       # Can include utility functions that are used across different features.
├── requirements.txt # Lists project dependencies.
```
**app/api/endpoints/**: Contains modules for each feature (user, product, payments).

**app/api/routers/**: Contains FastAPI routers, where each router corresponds to a feature.

**app/models/**: Contains modules defining database models for users, products, payments, etc.

**app/core/**: Contains core functionality like database management, dependencies, etc.

**app/utils/**: Can include utility functions that are used across different features.

**app/main.py**: Initializes the FastAPI app and brings together various components.

**tests/**: Houses your test cases.

**docs/**: Holds documentation files.

**scripts/**: Contains utility scripts.

**requirements.txt**: Lists project dependencies.


# Setup
1. The first thing to do is to clone the repository:
```sh
$ https://github.com/MahmudJewel/FastAPI-MongoDB-Template
```

2. Create a virtual environment to install dependencies in and activate it:
```sh
$ cd fastapi-booking-module
$ python -m venv venv
$ source venv/bin/activate
```
3. Then install the dependencies:
```sh
# for fixed version
(venv)$ pip install -r requirements.txt
```
Note the `(venv)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `venv`.

4. Now rename **.env.example** to **.env** and give the information on the .env file.
5. Then Run the project
```sh
(venv)$ uvicorn app.main:app --reload
```


# Tools
### Back-end
#### Language:
	Python

#### Frameworks:
	FastAPI
    pydantic
	
#### Other libraries / tools:
	beanie (MongoDB)
    motor
    starlette
    uvicorn
    python-jose
    python-dotenv
    google-auth

### Happy Coding

