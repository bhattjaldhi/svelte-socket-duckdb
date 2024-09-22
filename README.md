# Svelte Socket DuckDB

## Problem Statement

In many data-driven web applications, there's a need for real-time data analysis and visualization. Traditional client-server architectures often struggle with providing instantaneous updates and handling large datasets efficiently. This project aims to solve this problem by combining the power of Svelte for reactive UI updates, WebSockets for real-time communication, and DuckDB for fast, in-memory SQL analytics.

The Svelte Socket DuckDB project demonstrates a solution that allows users to perform SQL queries on a DuckDB database and receive results in real-time, all within a responsive web interface. This approach is particularly useful for scenarios where users need to explore and analyze data interactively, without the latency typically associated with traditional database queries.

## Features

- SQL query execution using DuckDB
- WebSocket communication for instant updates
- Reactive UI built with Svelte
- In-memory database processing for fast query results

## Prerequisites

- Node.js (v14 or later)
- npm (v6 or later)
- Python (v3.9 or later)
- Docker

## Project Structure

- **flask-server**: Flask application with Flask-SocketIO for real-time communication and DuckDB for database management.
- **svelte-app**: Svelte application using Flowbite UI framework for a modern table display and WebSocket communication.

## Installation and Setup

### Docker compose

1. Install docker-compose plugin
   
    ```bash
    sudo apt-get update
    sudo apt-get install docker-compose-plugin
    ```

2. Verify Docker installation

    ```bash
    docker compose version
    ```
1. Clone the repository
   
```bash 
git clone https://github.com/bhattjaldhi/svelte-socket-duckdb.git
```

2. Navigate to the folder
   
   ```bash
   cd svelte-socket-duckdb
   ```

3. To run in detached mode (in the background):
   
    ```bash
    docker compose up
    ```

4. To stop the containers:

    ```bash
    docker compose down
    ```



## Mermaid Sequence Diagram

Here’s a sequence diagram that explains the process:

```mermaid
sequenceDiagram
    participant F as Frontend (Svelte)
    participant N as Nginx
    participant B as Backend (Flask)
    participant D as Database (DuckDB)

    F->>N: GET /table to fetch table data
    N->>B: Forward request
    B->>RM: Check cache for table data
    alt Data in cache
        RM-->>B: Return cached data
    else Data not in cache
        B->>D: Query table data
        D-->>B: Return table data
        B->>RM: Cache table data
    end
    B-->>N: Send table data
    N-->>F: Forward table data

    F->>N: User performs changes in table (via WebSocket)
    N->>B: Forward changes
    B->>D: Update .db file with new cell value
    D-->>B: Confirm update
    B->>RM: Update cache
    RM->>RS: Replicate changes
    B->>N: Broadcast update to all clients
    N->>F: Forward update
    F-->>F: Reflect changes in all clients
