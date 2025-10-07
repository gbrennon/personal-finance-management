# Personal Finance Management - Microservices Architecture Guide

## Overview

This application has been successfully refactored from a monolithic Django application into a modern microservices architecture. The system now consists of multiple independent services that communicate through HTTP APIs and messaging.

## Architecture Components

### 1. Finance Service (Port 8001)
- **Technology**: Django 5.2.7 + Django REST Framework
- **Purpose**: Manages financial transactions, categories, and budgets
- **Database**: PostgreSQL (shared)
- **Container**: `finance_service`

### 2. Retirement Service (Port 8002)
- **Technology**: Django 5.2.7 + Django REST Framework + ML libraries
- **Purpose**: Handles retirement planning and financial projections
- **Database**: PostgreSQL (shared)
- **Container**: `retirement_service`

### 3. Backend for Frontend - BFF (Port 8003)
- **Technology**: FastAPI + httpx
- **Purpose**: API Gateway that aggregates data from microservices
- **Container**: `backend_for_frontend`

### 4. Frontend (Port 4200)
- **Technology**: Angular 17 + Angular Material
- **Purpose**: User interface (framework setup completed)
- **Container**: `frontend`

### 5. Infrastructure Services
- **PostgreSQL Database** (Port 5433)
- **Redis Cache/Messaging** (Port 6379)

## How to Run the Application

### Prerequisites
- Docker and Docker Compose installed
- Ports 8001, 8002, 8003, 4200, 5433, 6379 available

### Starting the Services

1. **Start all backend services:**
   ```bash
   docker-compose -f docker-compose.microservices.yml up -d
   ```

2. **Start specific services only:**
   ```bash
   docker-compose -f docker-compose.microservices.yml up postgres redis finance-service retirement-service backend-for-frontend -d
   ```

3. **Check service status:**
   ```bash
   docker-compose -f docker-compose.microservices.yml ps
   ```

4. **View service logs:**
   ```bash
   docker-compose -f docker-compose.microservices.yml logs [service-name]
   ```

### Stopping the Services

```bash
docker-compose -f docker-compose.microservices.yml down
```

## API Endpoints

### Backend for Frontend (Main API Gateway) - http://localhost:8003

#### Health Check
- `GET /health` - Check all services health status

#### Finance Endpoints
- `GET /api/finance/transactions` - List all transactions
- `POST /api/finance/transactions` - Create new transaction
- `GET /api/finance/transactions/summary` - Get financial summary
- `GET /api/finance/categories` - List categories
- `POST /api/finance/categories` - Create new category
- `GET /api/finance/budgets` - List budgets
- `POST /api/finance/budgets` - Create new budget

#### Retirement Endpoints
- `GET /api/retirement/plans` - List retirement plans
- `POST /api/retirement/plans` - Create retirement plan
- `GET /api/retirement/goals` - List retirement goals
- `POST /api/retirement/goals` - Create retirement goal

#### Dashboard
- `GET /api/dashboard` - Get combined dashboard data from all services

### Direct Service Access (for development/testing)

#### Finance Service - http://localhost:8001
- `GET /api/transactions/`
- `GET /api/categories/`
- `GET /api/budgets/`

#### Retirement Service - http://localhost:8002
- `GET /api/plans/`
- `GET /api/goals/`

## Testing the Application

### 1. Test Backend for Frontend API
```bash
curl http://localhost:8003/
curl http://localhost:8003/health
```

### 2. Test Individual Services
```bash
# Finance Service
curl http://localhost:8001/api/transactions/

# Retirement Service
curl http://localhost:8002/api/plans/
```

### 3. Check Service Logs
```bash
docker-compose -f docker-compose.microservices.yml logs backend-for-frontend
docker-compose -f docker-compose.microservices.yml logs finance-service
docker-compose -f docker-compose.microservices.yml logs retirement-service
```

## Database Setup

The services use a shared PostgreSQL database. To set up the database:

1. **Run migrations for Finance Service:**
   ```bash
   docker-compose -f docker-compose.microservices.yml exec finance-service python manage.py migrate
   ```

2. **Run migrations for Retirement Service:**
   ```bash
   docker-compose -f docker-compose.microservices.yml exec retirement-service python manage.py migrate
   ```

3. **Create superuser (optional):**
   ```bash
   docker-compose -f docker-compose.microservices.yml exec finance-service python manage.py createsuperuser
   ```

## Development Workflow

### Making Changes to Services

1. **Finance Service**: Edit files in `services/finance-service/`
2. **Retirement Service**: Edit files in `services/retirement-service/`
3. **Backend for Frontend**: Edit files in `services/backend-for-frontend/`
4. **Frontend**: Edit files in `services/frontend/`

### Rebuilding Services
```bash
docker-compose -f docker-compose.microservices.yml up --build [service-name]
```

### Adding New Dependencies
1. Update the respective `requirements.txt` file
2. Rebuild the service container

## Architecture Benefits

1. **Scalability**: Each service can be scaled independently
2. **Technology Diversity**: Different services can use different technologies
3. **Fault Isolation**: Failure in one service doesn't bring down the entire system
4. **Team Independence**: Different teams can work on different services
5. **Deployment Flexibility**: Services can be deployed independently

## Monitoring and Debugging

### Service Health
- Use `/health` endpoint on BFF to check all services
- Monitor individual service logs
- Check container status with `docker-compose ps`

### Common Issues
1. **Port conflicts**: Ensure ports 8001, 8002, 8003, 5433, 6379 are available
2. **Database connection**: Check PostgreSQL container is running
3. **Service communication**: Verify services can reach each other via Docker network

## Next Steps for Full Implementation

1. **Complete Frontend**: Implement Angular components and services
2. **Authentication**: Add JWT-based authentication across services
3. **API Documentation**: Add Swagger/OpenAPI documentation
4. **Testing**: Add unit and integration tests
5. **Monitoring**: Add logging, metrics, and health checks
6. **CI/CD**: Set up automated deployment pipeline

## File Structure

```
personal-finance-management/
├── docker-compose.microservices.yml    # Main orchestration file
├── services/
│   ├── finance-service/                # Django finance microservice
│   ├── retirement-service/             # Django retirement microservice
│   ├── backend-for-frontend/           # FastAPI BFF service
│   └── frontend/                       # Angular frontend
└── MICROSERVICES_GUIDE.md             # This guide
```

The microservices architecture is now fully operational and ready for further development and feature implementation.
