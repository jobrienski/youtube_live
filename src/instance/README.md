Put the secret config stuff in this folder with the environment name.

example:

```
export FLASK_ENV=development-docker
touch instance/development-docker.py

cat >> instance/development-docker.py

SQLALCHEMY_URL="postgres://blahblahblah"
