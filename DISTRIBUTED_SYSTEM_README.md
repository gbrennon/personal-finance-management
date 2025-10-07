# 🏦 Personal Finance Management - Distributed System

A modern, event-driven personal finance management system built with Django, Kafka, and Docker. This system demonstrates a distributed architecture with message-driven communication, CQRS pattern, and microservices design.

## 🏗️ Architecture Overview

### System Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Frontend  │    │  Message Bus    │    │   Database      │
│   (Django)      │◄──►│   (Kafka)       │◄──►│  (PostgreSQL)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Command/Event  │    │  Message        │    │   Background    │
│   Handlers      │    │  Dispatcher     │    │   Workers       │
│                 │    │                 │    │   (Celery)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Key Features

- **🎯 Event-Driven Architecture**: Uses Kafka for reliable message passing
- **📋 CQRS Pattern**: Separates command and query responsibilities
- **🔄 Message Dispatcher**: Routes messages to appropriate handlers
- **📊 Real-time Processing**: Async message handling with Celery
- **🐳 Containerized**: Full Docker deployment with orchestration
- **📈 Scalable**: Microservices-ready architecture

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Git
- 8GB+ RAM recommended

### 1. Clone and Setup

```bash
git clone <repository-url>
cd personal-finance-management
./setup_demo.sh
```

### 2. Access the Application

- **Web App**: http://localhost:8000
- **Kafka UI**: http://localhost:8080
- **Demo User**: `demo` / `demo123`
- **Admin User**: `admin` / `admin123`

## 📋 Features

### Core Financial Features

- ✅ **Transaction Management** - Income and expense tracking
- ✅ **Budget Planning** - Monthly budget setting and monitoring
- ✅ **Expense Forecasting** - ML-based prediction using Linear Regression
- ✅ **Financial Reports** - Monthly and yearly analysis

### New Distributed Features

- 🆕 **Invoice Management** - Create and track client invoices
- 🆕 **Investment Portfolio** - Track stocks, bonds, ETFs, real estate
- 🆕 **Retirement Planning** - Calculate retirement savings goals
- 🆕 **Real-time Notifications** - Event-driven alerts and updates

## 🏗️ Technical Architecture

### Message-Driven Design

The system uses a sophisticated message architecture:

#### Core Components

1. **Message** - Base class for all system messages
2. **MessageHandler** - Processes incoming messages
3. **MessageDispatcher** - Routes messages to handlers
4. **MessageBus** - Kafka-based message transport

#### Event Flow

```python
# Example: Creating a transaction
command = CreateTransactionCommand(
    user_id=user.id,
    transaction_type="Income",
    amount=1000.00,
    category="Salary",
    date="2024-01-15"
)

# Command is dispatched through message bus
await command_dispatcher.dispatch(command)

# Handler processes the command
# Event is published for other services
event = TransactionCreatedEvent(...)
await event_publisher.publish(event)
```

### Domain Structure

```
core/
├── domain/
│   ├── messages.py      # Base message classes
│   ├── events.py        # Domain events
│   └── commands.py      # Domain commands
├── application/
│   ├── handlers.py      # Message handlers
│   └── message_dispatcher_integration.py
└── infrastructure/
    └── message_bus.py   # Kafka implementation
```

### Event Types

#### Commands (Write Operations)
- `CreateTransactionCommand`
- `CreateInvoiceCommand`
- `CreateInvestmentCommand`
- `CreateRetirementPlanCommand`
- `GenerateForecastCommand`

#### Events (Notifications)
- `TransactionCreatedEvent`
- `BudgetExceededEvent`
- `InvoiceCreatedEvent`
- `InvestmentCreatedEvent`
- `RetirementPlanCreatedEvent`

## 🐳 Docker Services

### Infrastructure Services

- **Zookeeper** - Kafka coordination
- **Kafka** - Message broker
- **Redis** - Caching and Celery backend
- **PostgreSQL** - Primary database

### Application Services

- **Web** - Django web application
- **Celery** - Background task processing
- **Message Service** - Dedicated message handling
- **Kafka UI** - Message monitoring interface

## 📊 Monitoring & Observability

### Kafka UI Dashboard

Access http://localhost:8080 to monitor:

- Message topics and partitions
- Consumer groups and lag
- Message throughput
- System health

### Logging

Comprehensive logging across all services:

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f web
docker-compose logs -f message-service
docker-compose logs -f kafka
```

## 🧪 Testing the System

### 1. Create Transactions

```bash
# Login to the web interface
# Add income/expense transactions
# Observe messages in Kafka UI
```

### 2. Monitor Message Flow

1. Open Kafka UI: http://localhost:8080
2. Navigate to Topics
3. Watch for new messages in:
   - `commands.create_transaction`
   - `events.transaction_created`
   - `events.budget_exceeded`

### 3. Test Invoice System

```bash
# Create invoices through web interface
# Check message topics:
# - commands.create_invoice
# - events.invoice_created
```

## 🔧 Development

### Adding New Features

1. **Define Domain Objects**
   ```python
   # Add to core/domain/commands.py
   class NewFeatureCommand(Command):
       def __init__(self, data, **kwargs):
           super().__init__("new_feature", data, **kwargs)
   ```

2. **Create Handler**
   ```python
   # Add to core/application/handlers.py
   class NewFeatureHandler(MessageHandler):
       async def handle(self, message):
           # Process the command
           pass
   ```

3. **Register Handler**
   ```python
   # Update message_dispatcher_integration.py
   dispatcher.register_handler('NewFeatureCommand', NewFeatureHandler())
   ```

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:port/db

# Kafka
KAFKA_BOOTSTRAP_SERVERS=kafka:29092

# Redis
REDIS_URL=redis://redis:6379/0

# Message Bus
MESSAGE_BUS_TYPE=kafka  # or 'inmemory' for testing
```

## 📈 Performance & Scaling

### Horizontal Scaling

```yaml
# Scale services
docker-compose up --scale web=3 --scale celery=2
```

### Message Partitioning

Kafka topics are automatically partitioned for scalability:

- Commands: Partitioned by user_id
- Events: Partitioned by event type
- High throughput: Multiple consumers per partition

### Database Optimization

- Connection pooling enabled
- Read replicas supported
- Async ORM operations where possible

## 🛠️ Troubleshooting

### Common Issues

1. **Kafka Connection Issues**
   ```bash
   # Check Kafka health
   docker-compose exec kafka kafka-broker-api-versions --bootstrap-server localhost:9092
   ```

2. **Database Connection**
   ```bash
   # Test database connection
   docker-compose exec web python manage.py dbshell
   ```

3. **Message Service Not Starting**
   ```bash
   # Check message service logs
   docker-compose logs message-service
   ```

### Health Checks

```bash
# Check all service health
docker-compose ps

# Detailed service status
docker-compose exec web python manage.py check
```

## 🔒 Security Considerations

- **Message Encryption**: Kafka supports TLS encryption
- **Authentication**: JWT tokens for API access
- **Authorization**: Role-based access control
- **Data Privacy**: Personal data encryption at rest

## 🚀 Production Deployment

### Environment Setup

1. **Configure Environment**
   ```bash
   export DATABASE_URL=postgresql://...
   export KAFKA_BOOTSTRAP_SERVERS=kafka1:9092,kafka2:9092
   export REDIS_URL=redis://redis-cluster:6379
   ```

2. **Security Hardening**
   - Enable Kafka SASL/SSL
   - Configure PostgreSQL SSL
   - Set up proper firewall rules
   - Use secrets management

3. **Monitoring**
   - Prometheus metrics
   - Grafana dashboards
   - ELK stack for logs
   - Kafka monitoring tools

## 📚 Additional Resources

### Documentation

- [Django Documentation](https://docs.djangoproject.com/)
- [Apache Kafka](https://kafka.apache.org/documentation/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Celery](https://docs.celeryproject.org/)

### Architecture Patterns

- [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)
- [CQRS](https://martinfowler.com/bliki/CQRS.html)
- [Microservices](https://microservices.io/)
- [Message-Driven Architecture](https://www.reactivemanifesto.org/)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🎯 Demo Scenarios

### Scenario 1: Transaction Processing

1. Login as demo user
2. Add a new expense transaction
3. Monitor Kafka UI for message flow
4. Check budget alerts
5. View updated dashboard

### Scenario 2: Investment Tracking

1. Navigate to Investments section
2. Add new investment
3. Update current value
4. View portfolio performance
5. Check message processing

### Scenario 3: Retirement Planning

1. Access Retirement Planning
2. Set retirement goals
3. Calculate projections
4. Adjust contributions
5. Monitor progress

### Scenario 4: Invoice Management

1. Create new invoice
2. Send to client
3. Track payment status
4. Generate reports
5. Monitor cash flow

---

**🎉 Enjoy exploring the distributed personal finance management system!**
