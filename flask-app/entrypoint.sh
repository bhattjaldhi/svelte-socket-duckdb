#!/bin/bash
set -e

# Run database seeding script
python scripts/seed_db.py

# Check the command
if [ "$1" = "run" ]; then
    if [ "$FLASK_ENV" = "development" ]; then
        echo "Running in development mode..."
        python run.py
    else
        echo "Running in production mode..."
        gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:5000 run:app
    fi
elif [ "$1" = "bash" ]; then
    exec /bin/bash
else
    exec "$@"
fi