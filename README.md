# Fido Transactions API
RESTful API built with FastAPI - scope: transactions & user interactions

## Setup and Run Instructions

### Prerequisites

- Python 3.10+
- [Virtualenv](https://virtualenv.pypa.io/en/latest/)
- Docker

### Setup Steps

1. **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd fido-transaction-api
    ```

2. **Create a .env file (refer to .env.sample for content)**:
    ```bash 
    touch .env
    ```

3. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

4. **Install dependencies from the requirements.txt file**:
    ```bash
    pip install -r requirements.txt
    ```

5. **Run docker compose**:
    ```bash
    docker compose up --build
    ```

6. **API should be running on**:
    ```bash
    http://0.0.0.0:8000 # http://localhost:8000/
    ```

## Design and Architectural DecisionsDesicions