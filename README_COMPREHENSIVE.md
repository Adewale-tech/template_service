# Template Service - Comprehensive README

## Overview

**Template Service** is a microservice for managing notification templates in the HNG Distributed Notification System. It handles the storage, versioning, and rendering of email and push notification templates with support for variable substitution and multiple languages.

## Features

- ✅ **Template Management**: Create, read, update, and delete notification templates
- ✅ **Versioning**: Maintain version history of templates
- ✅ **Multi-language Support**: Templates in multiple languages (EN, ES, FR, DE, AR, ZH, PT)
- ✅ **Variable Substitution**: Fill templates with dynamic variables (e.g., {{name}}, {{order_id}})
- ✅ **Caching**: Redis-backed caching for improved performance
- ✅ **Message Queue**: RabbitMQ integration for async template operations
- ✅ **Circuit Breaker**: Fault tolerance with automatic recovery
- ✅ **Retry Logic**: Exponential backoff for failed operations
- ✅ **Health Checks**: `/health` endpoint for monitoring
- ✅ **Idempotency**: Prevent duplicate operations with request IDs
- ✅ **Correlation Tracking**: Distributed tracing with correlation IDs
- ✅ **API Documentation**: Auto-generated OpenAPI docs at `/docs`

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    API Gateway Service                       │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          │ HTTP/REST
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              Template Service (This Service)                 │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐   │
│  │              API Endpoints                           │   │
│  │  POST   /api/v1/templates                           │   │
│  │  GET    /api/v1/templates/{name}                    │   │
│  │  PUT    /api/v1/templates/{name}                    │   │
│  │  DELETE /api/v1/templates/{name}                    │   │
│  │  GET    /health                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                      │                                       │
│  ┌──────────────────┼──────────────────┐                   │
│  ▼                  ▼                  ▼                   │
│ [DB]            [Cache]          [Message Queue]          │
│PostgreSQL       Redis            RabbitMQ                │
│  └──────────────────┬──────────────────┘                   │
│                     │ Async Messaging                     │
│                     ▼                                       │
│              ┌─────────────────┐                           │
│              │ Email Service   │                           │
│              │ Push Service    │                           │
│              └─────────────────┘                           │
└─────────────────────────────────────────────────────────────┘
```

## Tech Stack

- **Framework**: FastAPI (Python 3.10+)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache**: Redis
- **Message Queue**: RabbitMQ
- **Containerization**: Docker & Docker Compose
- **Testing**: pytest, pytest-asyncio
- **CI/CD**: GitHub Actions

## Project Structure

```
template_service/
├── app/
│   ├── core/
│   │   ├── config.py           # Configuration settings
│   │   ├── logging_config.py    # Logging setup
│   │   ├── exceptions.py        # Custom exceptions
│   │   └── constants.py         # Application constants
│   ├── utils/
│   │   ├── circuit_breaker.py   # Circuit breaker pattern
│   │   ├── retry.py             # Retry logic with backoff
│   │   ├── correlation_id.py    # Distributed tracing
│   │   └── pagination.py        # Pagination utilities
│   ├── api/
│   │   └── v1/                  # API routes
│   ├── models.py                # SQLAlchemy models
│   ├── schemas.py               # Pydantic schemas
│   ├── crud.py                  # Database operations
│   ├── database.py              # Database setup
│   ├── dependencies.py          # FastAPI dependencies
│   └── main.py                  # Application entry point
├── services/
│   ├── cache.py                 # Redis cache service
│   └── messaging.py             # RabbitMQ messaging service
├── tests/
│   ├── unit/                    # Unit tests
│   ├── integration/             # Integration tests
│   ├── fixtures/                # Test fixtures
│   └── conftest.py              # Pytest configuration
├── scripts/
│   ├── debug.py                 # Debug utilities
│   ├── migrate.py               # Database migrations
│   └── health_check.py          # Health checks
├── .github/workflows/
│   └── ci-cd.yml                # GitHub Actions CI/CD
├── Dockerfile                   # Production Docker image
├── docker-compose.yml           # Local development setup
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Installation

### Prerequisites
- Python 3.10+
- Docker & Docker Compose
- PostgreSQL 14+
- Redis 7+
- RabbitMQ 3.11+

### Local Setup (Without Docker)

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/template_service.git
   cd template_service
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run database migrations**
   ```bash
   python scripts/migrate.py
   ```

6. **Run debug checks**
   ```bash
   python scripts/debug.py
   ```

7. **Start the service**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
   ```

### Docker Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/template_service.git
   cd template_service
   ```

2. **Create .env file**
   ```bash
   cp .env.example .env
   ```

3. **Start services**
   ```bash
   docker-compose up -d
   ```

4. **Check service health**
   ```bash
   curl http://localhost:8001/health
   ```

## API Endpoints

### Health Check
```http
GET /health
```
Response:
```json
{
  "success": true,
  "message": "Template Service is healthy and running.",
  "data": null,
  "meta": null
}
```

### Create Template
```http
POST /api/v1/templates
Content-Type: application/json

{
  "name": "welcome_email",
  "language": "en",
  "subject": "Welcome to {{company_name}}",
  "body": "Hello {{user_name}}, welcome to our service!",
  "template_type": "email",
  "status": "published"
}
```

### Get Latest Template
```http
GET /api/v1/templates/{name}?language=en
```

### Update Template
```http
PUT /api/v1/templates/{name}?language=en

{
  "subject": "New Subject",
  "body": "New Body {{variable}}"
}
```

### Delete Template
```http
DELETE /api/v1/templates/{name}?language=en
```

## Running Tests

### Run all tests
```bash
pytest tests/ -v
```

### Run specific test file
```bash
pytest tests/unit/test_models.py -v
```

### Run with coverage
```bash
pytest tests/ --cov=app --cov-report=html
```

### Run integration tests only
```bash
pytest tests/integration/ -v -m integration
```

## Database Migrations

### Create new migration
```bash
alembic revision --autogenerate -m "Add new column"
```

### Apply migrations
```bash
python scripts/migrate.py
```

## Debugging

### Run debug checks
```bash
python scripts/debug.py
```

This checks:
- Database connectivity
- Redis connectivity
- RabbitMQ connectivity
- Environment variables

### View logs
```bash
docker-compose logs -f template-service
```

### Access PostgreSQL
```bash
docker-compose exec postgres psql -U template_user -d template_db
```

### Access Redis
```bash
docker-compose exec redis redis-cli
```

### Access RabbitMQ Management
Visit: http://localhost:15672 (default: guest/guest)

## Performance Monitoring

### Metrics Tracked
- Template creation/update latency
- Cache hit rates
- Message queue depth
- Database query times
- API response times

### Health Checks
All services include `/health` endpoints for monitoring:
- **Status**: Service status
- **Database**: Database connectivity
- **Cache**: Redis connectivity
- **Message Queue**: RabbitMQ connectivity

## Error Handling

### Common Error Codes

| Code | Message | Status |
|------|---------|--------|
| TEMPLATE_NOT_FOUND | Template not found | 404 |
| TEMPLATE_DUPLICATE | Template already exists | 409 |
| INVALID_TEMPLATE | Invalid template data | 400 |
| VARIABLE_SUBSTITUTION_ERROR | Variable substitution failed | 400 |
| CACHE_ERROR | Cache operation failed | 503 |
| DATABASE_ERROR | Database operation failed | 503 |

### Retry Policy

- **Max Retries**: 3
- **Base Delay**: 1 second
- **Max Delay**: 60 seconds
- **Backoff**: Exponential (2^attempt)

### Circuit Breaker

- **Failure Threshold**: 5 failures
- **Recovery Timeout**: 60 seconds
- **States**: CLOSED → OPEN → HALF_OPEN

## Contributing

1. Create feature branch: `git checkout -b feature/amazing-feature`
2. Commit changes: `git commit -m 'Add amazing feature'`
3. Push to branch: `git push origin feature/amazing-feature`
4. Open Pull Request

### Code Standards

- Follow PEP 8
- Use type hints
- Write unit tests for new features
- Maintain > 80% code coverage

### Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Setup hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## Deployment

### Using Docker Compose (Development)
```bash
docker-compose up -d
```

### Using Docker (Production)
```bash
docker build -t template-service:latest .
docker run -d \
  -p 8001:8001 \
  --name template-service \
  -e DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/template_db \
  -e REDIS_URL=redis://redis:6379/0 \
  -e RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/ \
  template-service:latest
```

### CI/CD Pipeline

GitHub Actions automatically:
1. Runs linting and type checks
2. Runs unit tests
3. Builds Docker image
4. Pushes to registry
5. Deploys to production (on main branch)

## Monitoring & Logging

### Logging Format
- **JSON Format** (Production): Structured logs for ELK stack
- **Text Format** (Development): Human-readable logs

### Log Levels
- DEBUG: Detailed diagnostic info
- INFO: Confirmation that things are working
- WARNING: Warning conditions
- ERROR: Error conditions
- CRITICAL: Critical error conditions

### Correlation ID
All logs include `correlation_id` for request tracing across services:
```json
{
  "timestamp": "2024-01-15T10:30:45.123Z",
  "level": "INFO",
  "name": "app.api",
  "correlation_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Template created successfully"
}
```

## Troubleshooting

### Service won't start
```bash
# Check logs
docker-compose logs template-service

# Run debug script
python scripts/debug.py

# Check ports
netstat -an | grep 8001
```

### Database connection issues
```bash
# Test connection
python -c "from app.database import engine; print(engine)"

# Check environment variables
printenv | grep DATABASE_URL
```

### Redis connection issues
```bash
# Test connection
redis-cli ping

# Check Redis data
redis-cli KEYS '*'
redis-cli FLUSHDB  # Clear cache (dev only)
```

### RabbitMQ connection issues
```bash
# Check RabbitMQ status
docker-compose logs rabbitmq

# Access management UI
# http://localhost:15672 (guest/guest)
```

## License

This project is part of the HNG Internship Program.

## Support

For issues and questions:
- Create a GitHub issue
- Contact the team lead
- Check documentation at `/docs` (Swagger UI)

## Related Services

- **API Gateway Service**: Entry point for all requests
- **User Service**: Manages user data and preferences
- **Email Service**: Sends emails using templates
- **Push Service**: Sends push notifications using templates

---

**Last Updated**: November 13, 2025
**Version**: 1.0.0
**Maintainer**: Adewale-tech
