#!/bin/bash

cd "$(dirname "$0")"  # Ensure we are in user-auth-api

gunicorn -w 4 -b 0.0.0.0:5001 --chdir ./backend main:app
