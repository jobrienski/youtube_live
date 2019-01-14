#!/bin/bash

export FLASK_ENV="development"
export FLASK_APP=run_app.py 

${GUNICORN_COMMAND:-"../venv/bin/gunicorn"} \
        -c ./gunicorn.cfg                   \
        -w ${CONCURRENCY:-"2"} --chdir .    \
        -b 127.0.0.1:${FLASK_PORT:-"5000"} run_app:app
