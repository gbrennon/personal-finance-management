# Personal Finance Management System - User Guide

## Overview

This Personal Finance Management System has been completely refactored to use a modern service-based architecture with the following key features:

- **Service-Oriented Architecture**: Clean separation of concerns with dedicated services for each business operation
- **Repository Pattern**: Database operations abstracted through interfaces
- **Message Bus Integration**: Apache Kafka integration for event-driven architecture (with fallback mock for development)
- **Dependency Injection**: Proper IoC container for managing dependencies
- **New Features**: Retirement planning and cryptocurrency investment tracking

## Architecture Overview

### Service Layer
All business logic is encapsulated in service classes that follow the pattern:
- Each service has a single `execute()` method
- Services are injected with their dependencies (repositories, message bus)
- Examples: `RegisterTransactionService`, `CreateRetirementGoalService`, `RegisterCryptoInvestmentService`

### Repository Layer
Data access is abstracted through repository interfaces:
- `TransactionRepository`, `CategoryRepository`, `BudgetRepository`
- `RetirementGoalRepository`, `RetirementContributionRepository`, `CryptoInvestmentRepository`
- Django ORM implementations provided

### Message Bus
Event-driven communication using Apache Kafka:
- Events published for all major operations (transaction created, retirement contribution added, etc.)
- Mock implementation provided for development when Kafka is not available

## Getting Started

### 1. Setup and Installation

```bash
# Clone the repository
git clone <repository-url>
cd personal-finance-management

# Build and start the application
docker-compose up --build -d

# Run migrations
docker-compose exec web python manage.py migrate

# Setup demo data (optional but recommended)
docker-compose exec web python setup_demo.py
```

### 2. Access the Application

**Service-Based Interface (New):**
- URL: http://localhost:8000/service/dashboard/
- Demo Login: username `demo`, password `demo123`

**Original Interface (Legacy):**
- URL: http://localhost:8000/dashboard/
- Create your own user or use the demo account

## Features Guide

### 1. Dashboard
**URL:** `/service/dashboard/`

The main dashboard provides:
- **Financial Overview**: Total income, expenses, and savings
- **Quick Actions**: Easy access to add transactions and manage investments
- **Recent Transactions**: Last 10 transactions with type indicators
- **Navigation**: Access to all features through the top navigation bar

### 2. Transaction Management

#### Add Income
**URL:** `/service/add-income/`
- Select from predefined income categories (Salary, Freelance, etc.)
- Enter amount and date
- Automatically categorized and tracked

#### Add Expense
**URL:** `/service/add-expense/`
- Select from predefined expense categories (Rent, Groceries, etc.)
- Enter amount and date
- Budget alerts if you exceed monthly limits

### 3. Retirement Planning
**URL:** `/service/retirement/`

#### Features:
- **Set Retirement Goals**: Define target amount, target date, and monthly contribution
- **Track Progress**: Visual progress indicators showing current vs. target amounts
- **Add Contributions**: Record retirement account contributions
- **Goal Management**: Update goals as your situation changes

#### Creating a Retirement Goal:
1. Navigate to Retirement → Create Goal
2. Set your target retirement amount (e.g., $1,000,000)
3. Choose your target retirement date
4. Define monthly contribution amount
5. Enter current retirement savings (if any)

#### Adding Contributions:
1. Go to Retirement → Add Contribution
2. Select the retirement goal
3. Enter contribution amount and date
4. Add optional description
5. System automatically updates your progress

### 4. Cryptocurrency Investments
**URL:** `/service/crypto/`

#### Supported Cryptocurrencies:
- **Bitcoin (BTC)**
- **Ethereum (ETH)**

#### Features:
- **Portfolio Overview**: Total invested, current value, profit/loss
- **Investment Tracking**: Record purchases with quantity and price
- **Price Updates**: Update current prices to see real-time portfolio value
- **Sell Investments**: Record sales and calculate profits/losses

#### Adding Crypto Investments:
1. Navigate to Crypto → Add Investment
2. Select cryptocurrency type (BTC or ETH)
3. Enter investment amount and quantity purchased
4. Set purchase price and date
5. System calculates potential gains/losses when prices are updated

#### Updating Prices:
- Use the "Update Price" feature to set current market prices
- System automatically calculates current portfolio value and profit/loss
- Prices can be updated individually for each investment

### 5. Reports and Analytics

#### Monthly Reports
- Income vs. expenses by month
- Budget tracking and alerts
- Savings analysis

#### Forecasting
- Machine learning-based expense prediction
- Requires at least 2 months of data
- Predicts next 3 months of expenses

## System Administration

### Running Tests
```bash
# Test the service architecture
docker-compose exec web python test_services.py

# Run Django tests
docker-compose exec web python manage.py test
```

### Database Management
```bash
# Create migrations for model changes
docker-compose exec web python manage.py makemigrations

# Apply migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

### Demo Data Management
```bash
# Setup demo data
docker-compose exec web python setup_demo.py

# Access Django admin
# URL: http://localhost:8000/admin/
# Use superuser credentials
```

## API Architecture

### Service Classes

#### Transaction Services
- `RegisterTransactionService`: Create new transactions
- `GetUserTransactionsService`: Retrieve user transactions
- `UpdateTransactionService`: Modify existing transactions
- `DeleteTransactionService`: Remove transactions

#### Retirement Services
- `CreateRetirementGoalService`: Set up retirement goals
- `AddRetirementContributionService`: Record contributions
- `GetUserRetirementGoalsService`: Retrieve user goals
- `UpdateRetirementGoalService`: Modify goals

#### Crypto Services
- `RegisterCryptoInvestmentService`: Record crypto purchases
- `UpdateCryptoPriceService`: Update market prices
- `GetCryptoPortfolioSummaryService`: Portfolio overview
- `SellCryptoInvestmentService`: Record sales

### Event System

The system publishes events for major operations:
- `transaction.created`, `transaction.updated`, `transaction.deleted`
- `retirement_goal.created`, `retirement_contribution.added`
- `crypto_investment.created`, `crypto_price.updated`, `crypto_investment.sold`

## Troubleshooting

### Common Issues

1. **Kafka Connection Warnings**
   - Expected in development environment
   - System falls back to mock message bus
   - No impact on functionality

2. **Database Issues**
   - Run migrations: `docker-compose exec web python manage.py migrate`
   - Check container status: `docker-compose ps`

3. **Permission Errors**
   - Ensure Docker has proper permissions
   - Try rebuilding: `docker-compose up --build`

### Development

#### Adding New Features
1. Create domain entities in `finance/domain/entities.py`
2. Define repository interfaces in `finance/interfaces/repositories.py`
3. Implement Django repositories in `finance/repositories/django_repositories.py`
4. Create service classes in `finance/services/`
5. Wire up dependencies in `finance/infrastructure/container.py`
6. Create views in `finance/views_service.py`
7. Add URL patterns in `finance/urls_service.py`

#### Testing
- Unit tests for services should mock repositories and message bus
- Integration tests can use the test database
- Use the provided test script as a reference

## Security Considerations

- All views require authentication (`@login_required`)
- User data is isolated (services validate user ownership)
- Input validation through Django forms and service layer
- CSRF protection enabled
- SQL injection protection through Django ORM

## Performance Considerations

- Database queries optimized through repository pattern
- Lazy loading of related objects
- Pagination recommended for large datasets
- Consider caching for frequently accessed data

## Future Enhancements

Potential areas for expansion:
- Additional cryptocurrency support
- Advanced retirement planning calculations
- Investment portfolio analysis
- Mobile application API
- Real-time price feeds integration
- Advanced reporting and analytics
- Multi-currency support

## Support

For technical issues or questions:
1. Check the troubleshooting section
2. Review the system logs: `docker-compose logs web`
3. Verify database state through Django admin
4. Run the test suite to identify issues

---

**Version:** 2.0 (Service Architecture)  
**Last Updated:** October 2025  
**Compatibility:** Django 5.2+, Python 3.12+, Docker
