# Mantra - Study Analytics API

A FastAPI-based study tracking and analytics system that provides user study summaries with statistical analysis capabilities.

## Overview

Mantra is a RESTful API service that tracks user study records and provides analytical insights through time-series data aggregation and Simple Moving Average (SMA) calculations. The system supports multiple time granularities and offers JWT-based authentication for secure access.

## Features

- **User Management**: Track individual users and their study sessions
- **Record Tracking**: Store study records with word count and study time metrics
- **Time-Series Analytics**: Aggregate data by hour, day, week, or month
- **Simple Moving Average**: Calculate SMA for word count and study time trends
- **JWT Authentication**: Secure API endpoints with token-based authentication
- **PostgreSQL Integration**: Robust data persistence with async database operations
- **Docker Support**: Containerized deployment with Docker Compose

## Algorithm Explanation

### Simple Moving Average (SMA) Calculation

The core algorithm implements Simple Moving Average for smoothing time-series data:

```
SMA(n) = (x₁ + x₂ + ... + xₙ) / n
```

Where:
- `n` = window size (number of periods)
- `x₁, x₂, ..., xₙ` = data points in the window

**Implementation:**
```python
# Word Count SMA
word_count_sma = sum([record.total_words for record in records[i-n+1:i+1]]) / n

# Study Time SMA  
study_time_sma = sum([record.total_time for record in records[i-n+1:i+1]]) / n
```

**Pseudocode:**
```
FOR each record position i FROM (n-1) TO length(records):
    window = records[i-n+1 : i+1]
    word_count_sma = ROUND(SUM(window.word_counts) / n, 2)
    study_time_sma = ROUND(SUM(window.study_times) / n, 2)
    UPDATE record[i] WITH sma_values
END FOR
```

## API Endpoints

### Get User Summary
```
GET /api/v1/users/{user_id}/summary
```

**Parameters:**
- `user_id`: User identifier
- `start`: Start timestamp (Unix)
- `end`: End timestamp (Unix) 
- `granularity`: Time granularity (`hour`, `day`, `week`, `month`)
- `n` (optional): SMA window size

**Response:**
```json
{
  "summary": [
    {
      "date": "2024-01-01T00:00:00",
      "word_count": 1500,
      "study_time": 3600,
      "word_count_sma": 1450.5,
      "study_time_sma": 3500.2
    }
  ],
  "total": 1
}
```

## Installation & Setup

### Prerequisites
- Python 3.13+
- PostgreSQL 17
- Docker & Docker Compose (optional)

### Local Development

1. **Clone the repository**
```bash
git clone <repository-url>
cd mantra
```

2. **Install dependencies**
Install uv
```bash
# Installation guide: https://docs.astral.sh/uv/getting-started/installation/

# macOS/Linux
brew install uv
# or for system without Homebrew
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify installation
uv --version
```
Install python dependencies
```bash
uv sync
```

3. **Set up**
```bash
# Start service and postgreSQL with Docker
```bash
./setup_local_ut.sh

# Run migrations
cd scripts
alembic revision --autogenerate -m "init"
alembic upgrade head
```

4. **Create test users**
```bash
python scripts/create_users.py
```

5. **Run the application**
```bash
# Uvicorn
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
# fastapi
fastapi run main.py --port 8000
```

## Testing (Local)

```bash
# Run all tests
 pytest --log-level=INFO -v tests/

# Run with coverage
pytest --log-level=INFO -v --cov-report term:skip-covered --cov=./ tests/

# Run specific test file
pytest --log-level=INFO -v tests/service/test_user_service.py
```

## Project Structure

```
mantra/
├── src/
│   ├── api/v1/          # API endpoints and controllers
│   ├── core/            # Core utilities and context
│   ├── model/           # SQLAlchemy models
│   ├── repository/      # Data access layer
│   ├── service/         # Business logic
│   └── util/            # Utility functions
├── tests/               # Test suite
├── scripts/             # Database migrations and utilities
└── docker-compose.yml   # Container orchestration
```

## Configuration

Environment variables:
- `POSTGRES_HOST`: Database host
- `POSTGRES_PORT`: Database port  
- `POSTGRES_USER`: Database username
- `POSTGRES_PASSWORD`: Database password
- `POSTGRES_DB`: Database name

## 3 Ideas for Future Accuracy Improvements 

### Functionality
#### 1. Weighted Moving Average (WMA)
Replace SMA with WMA to give more importance to recent data points:
```
WMA = (w₁×x₁ + w₂×x₂ + ... + wₙ×xₙ) / (w₁ + w₂ + ... + wₙ)
```
This would provide more responsive trend analysis by emphasizing recent study patterns over older data.

### Implementation
#### 1. Pre-Aggregation of Raw Data with Async Tasks
Introduce asynchronous background tasks to preprocess raw data into coarser and more fundamental units. For example, if the current minimum granularity is at the hourly level, we can first consolidate study records into per-hour aggregates. This approach reduces the need for heavy real-time computation, thereby lowering CPU and memory consumption during queries.

#### 2. Enhanced Error Handling
Implement more robust error handling mechanisms to improve system resilience, ensuring that failures are properly captured, logged, and gracefully recovered without impacting overall service stability.

#### 3. Service and Database Metrics
Add monitoring metrics for both the service and the database. This will provide better visibility into resource utilization, performance trends, and potential bottlenecks, enabling proactive improvements and faster issue detection.
