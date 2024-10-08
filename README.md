# Fido Transactions API
RESTful API built with FastAPI - scope: transactions & user interactions

## Setup and Run Instructions

### Prerequisites

- Python 3.10+ 
- pip
- Virtualenv
- Docker

### Setup Steps

1. **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd fido-transaction-api
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Create a .env file refer to .evn.example**:
    ```bash
    touch .evn
    ```

3. **Install dependencies from the requirements.txt file**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run docker compose**:
    ```bash
    docker compose up --build
    ```

5. **API should be running on**:
    ```bash
    http://0.0.0.0:8000 # http://localhost:8000/
    ```

## Design and Architectural Decisions

### 1. API Design
- **RESTful API**: The API follows REST principles, making it intuitive and easy to use.

- **Status Codes**: Proper HTTP status codes are used to indicate the result of an API request (e.g., 200 for success, 404 for not found, 500 for server error).

### 2. Models
- **Pydantic Models**: Used Pydantic models for data validation and serialization. This ensures that the data conforms to the expected schema before processing.
  - Usage: [`TransactionModel`](app/models/transaction_model.py), [`AnalyticsModel`](app/models/analytics_model.py).

### 3. Database Connections
- **MongoDB**: Utilized MongoDB for its flexibility and scalability.
  - **AsyncIO Motor Client**: Used [`motor.motor_asyncio.AsyncIOMotorClient`](app/database/database.py) for asynchronous database operations, improving the performance of the API.
  - **Database Session Manager**: Implemented a session manager to handle database connections efficiently.
    - Usage: [`MongoDBSessionManager`](app/database/database.py).

### 4. Caching
- **Redis**: Integrated Redis for caching frequently accessed data to reduce database load and improve response times. Implemented strategies of cache updates and invalidation.
  - Usage: [`redis_client`](app/config/redis_config.py).

### 5. Error Handling
- **Custom Exceptions**: Defined custom exceptions to handle specific error scenarios gracefully.
  - Usage: [`ServiceError`](app/exceptions/exceptions.py), [`EntityDoesNotExistError`](app/exceptions/exceptions.py).
- **Exception Handlers**: Registered exception handlers to return meaningful error messages to the client.
  - Usage: [`service_error_handler`](app/exceptions/exception_handler.py).

### 6. Logging
- **Loguru**: Used Loguru for logging, providing better insights into the application's behavior and aiding in debugging.
  - Usage: [`logger`](app/config/logging.py).

### 7. Background Tasks
- **FastAPI Background Tasks**: Utilized FastAPI's background tasks to handle operations that do not need to block the main request-response cycle.
  - Usage: [`update_user_statistics`](app/tasks/background_tasks.py).

### 8. Scheduler
- **Analytics Computation Scheduler**: Implemented a scheduler to periodically compute and store analytics data.
  - Usage: [`start_scheduler`](app/tasks/scheduler.py).

### 9. Configuration Management
- **Environment Variables**: Managed configuration using environment variables to keep sensitive information secure and make the application configurable.
  - Usage: [`.env`](.env), [`config.py`](app/config/config.py).


## Strategies for Scaling to a Substantial User Base


### 1. Pagination of Endpoints
- **Strategy**: Implement pagination for endpoints that return large datasets.
- **Trade-offs**: 
  - **Pros**: Reduces server load and improves response times.
  - **Cons**: Adds complexity to the API and client-side code.

### 2. Database Indexing
- **Strategy**: Use indexing on frequently queried fields to speed up database operations.
- **Trade-offs**: 
  - **Pros**: Significantly improves query performance.
  - **Cons**: Increases storage requirements and can slow down write operations.

### 3. Event-Driven Architecture
- **Strategy**: Implement an event-driven architecture to decouple services and handle asynchronous tasks.
- **Trade-offs**: 
  - **Pros**: Improves scalability and fault tolerance.
  - **Cons**: Adds complexity to the system and requires robust event management.

### 4. Comprehensive Testing
- **Strategy**: Increase the scope of testing to include integration, performance, and stress tests.
- **Trade-offs**: 
  - **Pros**: Ensures the reliability and performance of the application under various conditions.
  - **Cons**: Requires more resources and time to implement and maintain.

### 5. Resilient Deployment Strategies
- **Strategy**: Use Kubernetes (K8s) for resilient and scalable deployments.
- **Trade-offs**: 
  - **Pros**: Provides automated scaling, self-healing, and efficient resource management.
  - **Cons**: Adds complexity to the deployment process and requires expertise in Kubernetes.


### Thank you!!