# Streaming Youtube Live Server and Front-end

## Description

This is a backend authentication server and youtube live api rest service
written in python. The authentication server does the following:
1. Handle oauth flow
2. Exchange auth code for auth token.
3. Exchange auth token for jwt token to be used by the front-end to
call the API.
More authorization details below.

## Installation

### Backend

#### Python


- Version: >= 3.6.4

- venv

```bash
$ python3 -mvenv ~/.slvenv # or wherever u want it
$ source ~/.slvenv/bin/activate
$ cp src/instance/development.py.template src/instance/development.py

```
- requirements

```bash
$ pip install -r requirements.txt
```
- Running Backend

cd src; FLASK_PORT=5000 FLASK_ENV=development python run_app.py

- Gunicorn

```bash
# from src
$ GUNICORN_COMMAND=~/.slvenv/bin/gunicorn ./run_guni_local.sh
```

- But it won't work until you set up the db and redis...(next)

#### Docker for postgresql and redis

- postgres and docker local instance

```bash
$ docker-compose -f ./dev_pg_redis.yml up -d
```

- Initialize Database

```bash
$ cd src
$ export FLASK_ENV=development
$ FLASK_APP=manage.py python manage.py db init
$ FLASK_APP=manage.py python manage.py db migrate
$ FLASK_APP=manage.py python manage.py db upgrade
```

### SwaggerUI

There is a swagger UI to the backend restapi at http://localhost:5000/doc/



## Front End

Front end is PROJECT_ROOT/frontend
Front end not finished - somewhat works, but the focus was more on the
back-end, authentication, etc.

Node 8 or greater

```bash
$ npm install
```

```bash
npm run dev
```

- Building for production

```bash

$ npm run build		# production build in dist

```

# Architecture Details

### Backend Description

#### Flask Restplus

The backend uses flask-restplus: https://flask-restplus.readthedocs.io/en/stable/,
which is a decent REST framework with swagger-ui integration. I've used a more
complicated version in the past with better argument parsing and marshmallow -
also better authorization and role support

#### SQLAlchemy

Database access is SQLAlchemy with Flask-SQLAlchemy 2.3.2. I don't however use 
Flask-SQLAlchemy's instantiation of models, rather declarative_base, because
it has more support for pooling and multi-threading.

#### Redis cache

Certain endpoints are cached with Flask-Caching, but I also use py-redis to 
directly cache jwt token blacklists.

#### Security and Authentication

I use backchannel authentication for social login. The front-end redirects to
the backend which handles the oauth authorization and access tokens. It then
exchanges them for a JWT access token with the identity being the google social
identity. It also returns a refresh token. There is a refresh endpoint for refreshing
tokens. 

I use Flask-JWT-Extended for the endpoint protection and JWT token generation.

##### Cookies

Tokens are returned in cookies for now. The frontend access the cookies, 
and then pulls the user info and deletes the cookie. 
If there is no cookie, there is a login button
displayed which redirects ot the backend oauth and jwt flow.
This isn't the ideal approach. It does lay the framework for what I would do in real
life, which is CSFR protection http://www.redotheweb.com/2015/11/09/api-security.html. 
It's not much more work to do this.
The jwt access token would be stored in an HTTP-only
session cookie. Then another token would be generated which would be returned to
the frontend. API requests would contain that second token in X-API-KEY and
verify it against the JWT access token. This makes it possible to eliminate 
access to the real token in javascript. This method is described here and supported
by Flask-JWT-Extended: 

https://flask-jwt-extended.readthedocs.io/en/latest/tokens_in_cookies.html


##### API Requests 

API requests that require a JWT token are marked with a lock in swaggerui. 
Authorization should be in the header with X-API-KEY: bearer <token>

