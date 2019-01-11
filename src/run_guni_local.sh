#!/bin/bash

export FLASK_ENV="integration"
export FLASK_APP=run_app.py 
GUNICORN_COMMAND=/home/jobrien/.venv/bin/gunicorn

${GUNICORN_COMMAND:-"../venv/bin/gunicorn"} \
        -c ./gunicorn.cfg                   \
        -w ${CONCURRENCY:-"2"} --chdir .    \
        -b 127.0.0.1:${FLASK_PORT:-"5000"} run_app:app
