#!/bin/bash

export FLASK_ENV="integration"
export FLASK_APP=run_app.py 

${GUNICORN_COMMAND:-"`pwd`/venv/bin/gunicorn"} \
        -c ./gunicorn.cfg                   \
        -w ${CONCURRENCY:-"4"} --chdir `pwd`/src    \
        -b 127.0.0.1:${FLASK_PORT:-"8081"} run_app:app

#        --keyfile ./ssl_keys/key.pem        \
