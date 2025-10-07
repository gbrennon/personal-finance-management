# Personal Finance Management Application

## Overview

This is a comprehensive Django-based personal finance management application that helps users track their finances across multiple domains: traditional finance, investments, retirement planning, and banking.

## Features

### 🏠 Core Finance Management
- **Income & Expense Tracking**: Add and categorize income and expenses
- **Budget Management**: Set monthly budgets and track spending
- **Financial Reports**: View detailed financial reports and forecasts
- **Dashboard**: Overview of your financial health

### 💰 Investment Management
- **Portfolio Tracking**: Track stocks, ETFs, mutual funds, and cryptocurrencies
- **Investment Types**: Support for various investment types
- **Transaction History**: Record buy/sell transactions with fees
- **Profit/Loss Tracking**: Real-time P&L calculations
- **Portfolio Analytics**: Comprehensive portfolio analysis

### 🏦 Retirement Planning
- **Retirement Accounts**: Manage 401(k), IRA, Roth IRA, and other accounts
- **Contribution Tracking**: Track employee and employer contributions
- **Retirement Goals**: Set and track retirement savings goals
- **Progress Monitoring**: Visual progress tracking with percentages
- **Retirement Calculator**: Calculate savings needed for retirement

### 🏛️ Banking Management
- **Multiple Account Types**: Checking, savings, credit cards, loans, mortgages
- **Transaction Management**: Track all banking transactions
- **Account Balances**: Real-time balance tracking
- **Transfer Management**: Record transfers between accounts
- **Institution Management**: Manage multiple banking institutions

## Technology Stack

- **Backend**: Django 5.2.7
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Frontend**: Bootstrap 5.3.0 with responsive design
- **Containerization**: Docker with Docker Compose
- **Python**: 3.12

## Installation & Setup

### Prerequisites
- Docker and Docker Compose installed
- Git

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd personal-finance-management
   ```

2. **Build and start the application**:
   ```bash
   docker-compose up --build -d
   ```

3. **Run database migrations**:
   ```bash
   docker exec personal_finance_app python manage.py migrate
   ```

4. **Set up demo data** (optional but recommended):
   ```bash
   docker exec personal_finance_app python manage.py setup_demo
   ```

5. **Access the application**:
   - Open your browser and go to `http://localhost:8000`
   - Login with demo credentials: `demo` / `demo123`

### Manual Setup (without demo data)

1. **Create a superuser**:
   ```bash
   docker exec personal_finance_app python manage.py createsuperuser
   ```

2. **Access admin panel**:
   - Go to `http://localhost:8000/admin`
   - Login with your superuser credentials

## Application Structure

### Django Apps

1. **finance** - Core financial management
   - Models: Category, Transaction, Budget
   - Features: Income/expense tracking, budgeting, reports

2. **investments** - Investment portfolio management
   - Models: InvestmentType, Investment, InvestmentTransaction, Portfolio
   - Features: Portfolio tracking, P&L calculations, investment analytics

3. **retirement** - Retirement planning
   - Models: RetirementAccount, RetirementContribution, RetirementGoal, RetirementProjection, SocialSecurityEstimate
   - Features: Retirement account management, goal setting, progress tracking

4. **banks** - Banking and account management
   - Models: BankInstitution, BankAccount, BankTransaction, BankTransfer, RecurringTransaction, BankAlert
   - Features: Multi-bank account management, transaction tracking, transfers

### Key Features

#### Navigation
- **Responsive navbar** with dropdown menus
- **Quick access** to all major features
- **User authentication** with login/logout

#### Dashboard Views
Each app has its own dashboard showing:
- **Summary cards** with key metrics
- **Recent activity** lists
- **Quick action buttons**
- **Data visualization** (charts and progress bars)

#### Data Management
- **CRUD operations** for all major entities
- **Form validation** and error handling
- **User-specific data** isolation
- **Bulk operations** where appropriate

## Usage Guide

### Getting Started

1. **Register/Login**: Create an account or use demo credentials
2. **Explore Dashboards**: Visit each section to understand the layout
3. **Add Data**: Start by adding your accounts, investments, etc.
4. **Set Goals**: Configure your financial and retirement goals
5. **Track Progress**: Regularly update your data to track progress

### Core Workflows

#### Finance Management
1. **Set up categories**: Create income and expense categories
2. **Add transactions**: Record your income and expenses
3. **Set budgets**: Create monthly budgets
4. **Review reports**: Check your financial reports regularly

#### Investment Tracking
1. **Add investment types**: Set up different investment categories
2. **Record investments**: Add your current holdings
3. **Track transactions**: Record buy/sell activities
4. **Monitor performance**: Review P&L and portfolio analytics

#### Retirement Planning
1. **Add accounts**: Set up your retirement accounts
2. **Set goals**: Define your retirement objectives
3. **Track contributions**: Record regular contributions
4. **Monitor progress**: Check your retirement readiness

#### Banking Management
1. **Add institutions**: Set up your banks
2. **Create accounts**: Add all your bank accounts
3. **Record transactions**: Track all banking activities
4. **Manage transfers**: Record money movements between accounts

## Demo Data

The application includes a comprehensive demo setup command that creates:

- **Demo user**: Username `demo`, Password `demo123`
- **Sample categories**: Income and expense categories
- **Transaction history**: 12 months of income, 90 days of expenses
- **Investment portfolio**: Sample stocks, ETFs, and crypto
- **Retirement accounts**: 401(k), IRA, and Roth IRA with contributions
- **Bank accounts**: Checking, savings, and credit card accounts
- **Transaction data**: 30 days of banking transactions

### Running Demo Setup

```bash
# Use default demo user
docker exec personal_finance_app python manage.py setup_demo

# Or specify custom credentials
docker exec personal_finance_app python manage.py setup_demo --username myuser --password mypass
```

## Development

### Project Structure
```
personal-finance-management/
├── financeapp/          # Django project settings
├── finance/             # Core finance app
├── investments/         # Investment management app
├── retirement/          # Retirement planning app
├── banks/              # Banking management app
├── templates/          # Shared templates
├── static/            # Static files (CSS, JS, images)
├── requirements.txt   # Python dependencies
├── Dockerfile        # Docker configuration
├── docker-compose.yml # Docker Compose configuration
└── manage.py         # Django management script
```

### Key Models

#### Finance App
- **Category**: Income/expense categories
- **Transaction**: Financial transactions
- **Budget**: Monthly budgets

#### Investments App
- **InvestmentType**: Types of investments
- **Investment**: Individual investment holdings
- **InvestmentTransaction**: Buy/sell transactions

#### Retirement App
- **RetirementAccount**: Retirement account details
- **RetirementContribution**: Contribution records
- **RetirementGoal**: Retirement planning goals

#### Banks App
- **BankInstitution**: Banking institutions
- **BankAccount**: Individual bank accounts
- **BankTransaction**: Banking transactions

### Adding New Features

1. **Models**: Define new models in the appropriate app
2. **Views**: Create views for CRUD operations
3. **Templates**: Design user interfaces
4. **URLs**: Configure URL routing
5. **Forms**: Create forms for data input
6. **Tests**: Write tests for new functionality

## Deployment

### Production Considerations

1. **Database**: Switch to PostgreSQL for production
2. **Static Files**: Configure static file serving
3. **Security**: Update SECRET_KEY and security settings
4. **Environment Variables**: Use environment-specific settings
5. **SSL**: Configure HTTPS
6. **Backup**: Implement database backup strategy

### Environment Variables

Create a `.env` file for production:
```env
DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost/dbname
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## Troubleshooting

### Common Issues

1. **Database Permission Errors**:
   ```bash
   rm -f db.sqlite3
   docker exec personal_finance_app python manage.py migrate
   ```

2. **Container Issues**:
   ```bash
   docker-compose down
   docker-compose up --build -d
   ```

3. **Static Files Not Loading**:
   ```bash
   docker exec personal_finance_app python manage.py collectstatic
   ```

### Logs and Debugging

```bash
# View application logs
docker logs personal_finance_app

# Access container shell
docker exec -it personal_finance_app bash

# Django shell
docker exec -it personal_finance_app python manage.py shell
```

## Support and Maintenance

### Regular Maintenance

1. **Database Backups**: Regular database backups
2. **Updates**: Keep dependencies updated
3. **Security**: Regular security updates
4. **Monitoring**: Monitor application performance
5. **User Feedback**: Collect and implement user feedback

### Backup Commands

```bash
# Backup database
docker exec personal_finance_app python manage.py dumpdata > backup.json

# Restore database
docker exec personal_finance_app python manage.py loaddata backup.json
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For support or questions, please contact the development team or create an issue in the repository.

---

**Happy Financial Management!** 💰📊📈
