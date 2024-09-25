#!/bin/bash
set -e

# Run database seeding script
python scripts/seed_db.py

# Check the command and environment
if [ "$1" = "run" ]; then
    if [ "$FLASK_ENV" = "development" ]; then
        echo "Running in development mode..."
        python run.py
    elif [ "$FLASK_ENV" = "production" ]; then
        echo "Running in production mode..."
        gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:5000 run:app
    elif [ "$FLASK_ENV" = "test" ]; then
        echo "Running tests..."
        pytest
    else
        echo "Unknown FLASK_ENV: $FLASK_ENV"
        exit 1
    fi
elif [ "$1" = "bash" ]; then
    exec /bin/bash
else
    exec "$@"
fi