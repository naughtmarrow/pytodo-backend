## Pytodo
___
### A todo app made in python
This repository contains the backend for the Pytodo app.

### Installation
#### Requirements:

- python >= 3.11
- A postgresql database

#### .env
The following variables are required to be set by the env
- DB_NAME: The name of the postgres database
- DB_USER: The name of the user with the appropriate privileges (SELECT, UPDATE, INSERT, DELETE) + (CREATE, USAGE, CONNECT, LOGIN, depending on your setup and needs)
- DB_PASSWORD: The password for said user
- DB_SCHEMA: The specific schema if needed
- DB_HOST: The hostname for the db connection
- DB_PORT: The port for the db connection
- PROTOCOL: Set to http or https if able
- SECRET_KEY: A secret key for usage in flask

#### Setup
The setup can be installed automatically with poetry. Make sure to enable your virtual environment if needed.

> [!CAUTION]
> This server is still in development, not recommended for deployment purposes.

```
python -m venv .venv
source ./.venv/bin/activate
poetry install
```

#### Run
The make file contains 2 methods for running

Running through werkzeug (not recommended for deployment):
```
make run
```

Running through gunicorn:
```
make run-hosted
```

> [!WARNING]
> The server relies on a reverse proxy for rate limiting. Make sure to double check security features before deploying

### Endpoints
#### General endpoints:
- `GET /csrf`: Use if you need to obtain a csrf token manually.
- `GET /`: Returns a hello world to check if server is up.

> [!NOTE]
> This will change to a standard health check endpoint in the future

#### User endpoints:
For user and session management.
- `POST /users/login`: Logs in a user if credentials match. Expects a json object with the username and password of the user to be logged in.
```
{
  "username": [username],
  "password": [password]
}
```
- `GET /users/logout`: Logs out the user. Requires Login.
- `POST /users`: Creates a new user in the database. Expects a json object with the username and password of the user to be registered in. Requires Login.
```
{
  "username": [username],
  "password": [password]
}
```

> [!WARNING]
> This system is set to change to allow for other things like password confirmation and other kinds of auth.

- `PUT /users`: Modifies the logged in user in the database. Expects a json object with the username to change. Requires Login.
```
{
  "username": [new_username],
}
```

> [!NOTE]
> This system is also set to change in the future once more features for the users are implemented.

- `DELETE /users`: Deletes the user data from the database and logs them out. Requires Login.

#### Todo endpoints:
- `GET /todos`: Returns the list of todos associated with the logged in user. Requires Login.
- `POST /todos`: Creates a new todo object in database associated with the logged in user. Expects a json object with the following format. Requires Login
```
{
  "description": [the title of the todo],
  "date_due": [date in iso format],
  "priority": [a number from 1 to 4 (urgent, important, normal, optional)],
  "completed": [a boolean value]
}
```

- `PUT /todos`: Updates the todo object based on the previous information. Expects a json object with the information available to the frontend on the todo.
```
{
  "id": [the id of the todo as given by GET /todos]
  "description": [the title of the todo],
  "date_created": [date in iso format],
  "date_due": [date in iso format],
  "priority": [a number from 1 to 4 (urgent, important, normal, optional)],
  "completed": [a boolean value]
}
```

- `DELETE /todos/:td_id`: Deletes a given todo. Requires the id of the todo as a url parameter.
