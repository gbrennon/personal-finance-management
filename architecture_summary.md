# Architecture Summary of Personal Finance Management Application

## Overview
This document summarizes the architecture and key approaches used in the personal finance management application.

## Technologies and Frameworks
- **Web Framework**: Django (version 5.2)
- **Database**: PostgreSQL (version 13)
- **Containerization**: Docker and Docker Compose
- **Dependency Management**: Python `pip` with `requirements.txt`

## Docker and Docker Compose Configuration
### Services
- **PostgreSQL Service (`db`)**:
  - Image: `postgres:13`
  - Environment variables for database configuration:
    - `POSTGRES_DB`: `finance_db`
    - `POSTGRES_USER`: `finance_user`
    - `POSTGRES_PASSWORD`: `finance_password`
  - Volume for data persistence: `postgres_data` mapped to `/var/lib/postgresql/data`
  - Port mapping: `5432:5432`
  - Network: `finance_network`
  - Health-check: `pg_isready -U postgres` every 5 seconds

- **Django Application Service (`web`)**:
  - Build context: Current directory (`.`)
  - Command: `python manage.py runserver 0.0.0.0:8000`
  - Volume for source code: Current directory mapped to `/code`
  - Port mapping: `8000:8000`
  - Depends on: `db` service
  - Environment variable: `DJANGO_SETTINGS_MODULE=financeapp.settings`
  - Network: `finance_network`

### Network
- A bridge network named `finance_network` is used to allow communication between the `db` and `web` services.

### Volumes
- `postgres_data`: A named volume for persistent storage of PostgreSQL data.

## Django Settings
### Database Configuration
The application is configured to use PostgreSQL with the following settings:
- **Engine**: `django.db.backends.postgresql`
- **Name**: `finance_db`
- **User**: `finance_user`
- **Password**: `finance_password`
- **Host**: `db` (resolvable within the Docker network)
- **Port**: `5432`

### Installed Apps
- `django_extensions`
- `django.contrib.admin`
- `django.contrib.auth`
- `finance` (custom app)
- Other Django contrib apps for sessions, messages, etc.

### Key Configuration
- `DEBUG = True`
- `ALLOWED_HOSTS = ["*"]`
- Static files URL: `static/`

## Project Dependencies (`requirements.txt`)
- Django (`~5.2`)
- `django-extensions`
- `gunicorn` (for production server)
- `pandas` (data manipulation)
- `scikit-learn` (machine learning capabilities)
- `matplotlib` (data visualization)
- `numpy` (numerical operations)
- `psycopg2-binary` (PostgreSQL adapter for Python)

## Data Models (`finance/models.py`)
### Category Model
- Represents income and expense categories.
- Fields:
  - `user`: Foreign key to Django's User model.
  - `name`: Name of the category.
  - `transaction_type`: Either 'Income' or 'Expense'.
- Constraints:
  - Unique together: `user`, `name`, `transaction_type`.

### Transaction Model
- Represents financial transactions.
- Fields:
  - `user`: Foreign key to Django's User model.
  - `transaction_type`: Either 'Income' or 'Expense'.
  - `amount`: Decimal field for the transaction amount.
  - `category`: Foreign key to the Category model.
  - `date`: Date of the transaction.

### Budget Model
- Represents user budgets.
- Fields:
  - `user`: Foreign key to Django's User model.
  - `amount`: Decimal field for the budget amount (nullable).
  - `month`: Integer for the month.
  - `year`: Integer for the year.
- Constraints:
  - Unique together: `user`, `month`, `year`.

## Summary of Architecture Approaches
1. **Microservices Architecture**: The application uses Docker Compose to manage multiple services (PostgreSQL and Django) in separate containers, promoting isolation and scalability.
2. **Persistent Storage**: Docker volumes are used for PostgreSQL data to ensure persistence across container restarts.
3. **Network Isolation**: A dedicated Docker network (`finance_network`) ensures secure and efficient communication between services.
4. **Health Checks**: The PostgreSQL service includes a health-check to ensure it is ready before the Django application starts, improving reliability.
5. **Modular Design**: The Django application is structured with a custom `finance` app, separating concerns and making the codebase maintainable.
6. **Data Modeling**: The models are designed to support key features such as categorizing transactions, tracking budgets, and associating data with specific users.

## Next Steps
- Ensure that the Docker network is correctly configured so that the `db` hostname is resolvable from the `web` service.
- Test the application thoroughly to confirm that it can connect to the PostgreSQL database and function as expected.
- Consider adding more robust error handling and logging for production readiness.
