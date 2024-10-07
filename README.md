# Fido Transactions API
RESTful API build with FastAPI - scope: transactions &amp; user interactions

## Setup and Run Instructions

### Prerequisites

- Python 3.8+
- [Virtualenv](https://virtualenv.pypa.io/en/latest/)
- Docker

### Setup Steps

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd fido-transaction-api

1. **create a .env file (refer to .evn.sample for content)**:
    ```bash 
    touch .evn

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .venv\Scripts\activate

2. **Install dependencies from the requirements.txt file**:
    ```bash
    pip install -r requirements.txt

3. **Run docker compose**:
    ```bash
    docker compose build
    dcoker compose up

4. **API should be running on**:
    ```bash
    http://0.0.0.0:8000