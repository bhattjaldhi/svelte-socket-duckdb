This Flask application serves as the backend for the Svelte Socket DuckDB project. It provides API endpoints for data management and real-time communication using WebSockets.

Table of Contents
-----------------

- [Table of Contents](#table-of-contents)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Development](#development)
- [Production](#production)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

Prerequisites
-------------
-   Docker
-   Docker Compose
-   Python 3.12+

Installation
------------

1.  Clone the repository:

    ```bash 
    git clone https://github.com/bhattjaldhi/svelte-socket-duckdb.git 
    cd svelte-socket-duckdb/flask-app 
    ```

2.  Copy the example environment file:

    ```bash 
    cp .env.example .env 
    ```

3.  Edit the `.env` file and set the appropriate values for your environment.

Development
-----------

To run the Flask app in development mode:

1.  Build and start the Docker container:

    ```bash 
    docker-compose up --build 
    ```

2.  The Flask app will be available at `http://localhost:5000`.
3.  To stop the container, press `Ctrl+C` in the terminal where docker-compose is running.

Production
----------

To run the Flask app in production mode:

1.  Create a `.env.prod` file with production-specific environment variables.
2.  Build and start the Docker container:

    ```bash 
    docker-compose -f docker-compose.yml up --build -d
    ```

3.  The Flask app will be running in the background. To view logs:

    ```bash 
    docker-compose logs -f 
    ```

4.  To stop the container:

    ```bash 
    docker-compose down
    ```

Testing
-------

To run the test suite:

1.  Create a `.env.test` file with test-specific environment variables.
2.  Run the tests using Docker:

    ```bash 
    docker-compose -f docker-compose.yml up --build
    ```

3.  The test results will be displayed in the console output.

Project Structure
-----------------

```
flask-app/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── utils/
├── tests/
├── scripts/
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh
├── poetry.lock
├── pyproject.toml
├── README.md
```

Contributing
------------

1.  Fork the repository
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request
