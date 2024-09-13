# Real-Time Editable Table with Flask and Svelte

This project demonstrates how to create a real-time editable table using Flask as the backend and Svelte for the frontend. Changes made to the table are sent to the backend via WebSockets and the database is updated accordingly. All connected clients receive updates in real-time.

## Project Structure

- **Backend**: Flask application with Flask-SocketIO for real-time communication and DuckDB for database management.
- **Frontend**: Svelte application using Flowbite UI framework for a modern table display and WebSocket communication.

## Installation and Setup

### Backend

1. **Create a Virtual Environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

2. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

### Frontend

1. **Setup Svelte Project**

    ```bash
    npx degit sveltejs/template svelte-app
    cd svelte-app
    npm install
    ```
2. **Run the Svelte Application**

    ```bash
    npm run dev
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
