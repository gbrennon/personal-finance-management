#!/bin/bash

# Personal Finance Management - Distributed System Demo Setup
# This script sets up the entire distributed system for demonstration

set -e  # Exit on any error

echo "🚀 Setting up Personal Finance Management Distributed System Demo"
echo "=================================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}$1${NC}"
}

# Check if Docker and Docker Compose are installed
check_dependencies() {
    print_header "Checking dependencies..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_status "Docker and Docker Compose are installed ✓"
}

# Clean up any existing containers
cleanup_existing() {
    print_header "Cleaning up existing containers..."
    
    docker-compose down --volumes --remove-orphans 2>/dev/null || true
    docker system prune -f 2>/dev/null || true
    
    print_status "Cleanup completed ✓"
}

# Build and start services
start_services() {
    print_header "Building and starting services..."
    
    print_status "Building Docker images..."
    docker-compose build --no-cache
    
    print_status "Starting infrastructure services (Kafka, Redis, PostgreSQL)..."
    docker-compose up -d zookeeper kafka redis db
    
    print_status "Waiting for services to be ready..."
    sleep 30
    
    print_status "Starting application services..."
    docker-compose up -d web celery message-service kafka-ui
    
    print_status "All services started ✓"
}

# Wait for services to be healthy
wait_for_services() {
    print_header "Waiting for services to be healthy..."
    
    local max_attempts=60
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if docker-compose ps | grep -q "Up (healthy)"; then
            print_status "Services are healthy ✓"
            return 0
        fi
        
        print_status "Attempt $attempt/$max_attempts - Waiting for services..."
        sleep 5
        ((attempt++))
    done
    
    print_warning "Services may not be fully healthy, but continuing..."
}

# Setup database
setup_database() {
    print_header "Setting up database..."
    
    print_status "Running database migrations..."
    docker-compose exec -T web python manage.py makemigrations
    docker-compose exec -T web python manage.py migrate
    
    print_status "Creating superuser..."
    docker-compose exec -T web python manage.py shell << 'EOF'
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Superuser created: admin/admin123")
else:
    print("Superuser already exists")
EOF
    
    print_status "Database setup completed ✓"
}

# Load sample data
load_sample_data() {
    print_header "Loading sample data..."
    
    docker-compose exec -T web python manage.py shell << 'EOF'
from django.contrib.auth.models import User
from finance.models import Category, Transaction, Budget, Invoice, Investment, RetirementPlan
from decimal import Decimal
from datetime import date, timedelta
import random

# Get or create demo user
user, created = User.objects.get_or_create(
    username='demo',
    defaults={
        'email': 'demo@example.com',
        'first_name': 'Demo',
        'last_name': 'User'
    }
)
if created:
    user.set_password('demo123')
    user.save()
    print("Demo user created: demo/demo123")

# Create categories
income_categories = ['Salary', 'Freelance', 'Investment Returns', 'Bonus']
expense_categories = ['Rent', 'Groceries', 'Transportation', 'Entertainment', 'Utilities']

for cat_name in income_categories:
    Category.objects.get_or_create(
        user=user,
        name=cat_name,
        transaction_type='Income'
    )

for cat_name in expense_categories:
    Category.objects.get_or_create(
        user=user,
        name=cat_name,
        transaction_type='Expense'
    )

# Create sample transactions
income_cats = Category.objects.filter(user=user, transaction_type='Income')
expense_cats = Category.objects.filter(user=user, transaction_type='Expense')

# Create transactions for the last 6 months
for i in range(180):  # 6 months of data
    transaction_date = date.today() - timedelta(days=i)
    
    # Create some income transactions
    if random.random() < 0.1:  # 10% chance of income per day
        Transaction.objects.get_or_create(
            user=user,
            transaction_type='Income',
            amount=Decimal(random.uniform(1000, 5000)),
            category=random.choice(income_cats),
            date=transaction_date
        )
    
    # Create some expense transactions
    if random.random() < 0.3:  # 30% chance of expense per day
        Transaction.objects.get_or_create(
            user=user,
            transaction_type='Expense',
            amount=Decimal(random.uniform(10, 500)),
            category=random.choice(expense_cats),
            date=transaction_date
        )

# Create sample budgets
for month in range(1, 13):
    Budget.objects.get_or_create(
        user=user,
        month=month,
        year=2024,
        defaults={'amount': Decimal(random.uniform(2000, 4000))}
    )

# Create sample invoices
for i in range(5):
    Invoice.objects.get_or_create(
        user=user,
        invoice_number=f'INV-{user.id}-{i+1:04d}',
        defaults={
            'client_name': f'Client {i+1}',
            'client_email': f'client{i+1}@example.com',
            'amount': Decimal(random.uniform(500, 5000)),
            'due_date': date.today() + timedelta(days=random.randint(7, 60)),
            'description': f'Sample invoice {i+1}',
            'status': random.choice(['draft', 'sent', 'paid'])
        }
    )

# Create sample investments
investment_types = ['stocks', 'bonds', 'mutual_funds', 'etf', 'real_estate']
for i, inv_type in enumerate(investment_types):
    Investment.objects.get_or_create(
        user=user,
        name=f'{inv_type.title()} Investment {i+1}',
        defaults={
            'investment_type': inv_type,
            'amount_invested': Decimal(random.uniform(1000, 10000)),
            'current_value': Decimal(random.uniform(1000, 12000)),
            'expected_return_rate': Decimal(random.uniform(5, 15)),
            'risk_level': random.choice(['low', 'medium', 'high']),
            'purchase_date': date.today() - timedelta(days=random.randint(30, 365)),
            'notes': f'Sample {inv_type} investment'
        }
    )

# Create retirement plan
RetirementPlan.objects.get_or_create(
    user=user,
    defaults={
        'target_retirement_amount': Decimal(1000000),
        'current_age': 35,
        'target_retirement_age': 65,
        'monthly_contribution': Decimal(1000),
        'current_savings': Decimal(50000),
        'expected_annual_return': Decimal(7.0)
    }
)

print("Sample data loaded successfully!")
EOF
    
    print_status "Sample data loaded ✓"
}

# Display service information
show_services() {
    print_header "Service Information"
    echo ""
    print_status "🌐 Web Application: http://localhost:8000"
    print_status "   - Demo User: demo / demo123"
    print_status "   - Admin User: admin / admin123"
    echo ""
    print_status "📊 Kafka UI: http://localhost:8080"
    print_status "   - Monitor message queues and topics"
    echo ""
    print_status "🐳 Docker Services:"
    docker-compose ps
    echo ""
}

# Display demo guide
show_demo_guide() {
    print_header "Demo Guide"
    echo ""
    echo "1. 🏠 Access the application at http://localhost:8000"
    echo "2. 🔐 Login with demo/demo123 or admin/admin123"
    echo "3. 📈 Explore the dashboard with sample data"
    echo "4. 💰 Add new transactions and see real-time updates"
    echo "5. 📋 Create invoices for clients"
    echo "6. 💼 Manage investment portfolio"
    echo "7. 🏖️  Plan for retirement"
    echo "8. 📊 Monitor Kafka messages at http://localhost:8080"
    echo ""
    print_status "The system uses a distributed architecture with:"
    echo "  - 🎯 Event-driven messaging with Kafka"
    echo "  - 🔄 Command/Query separation"
    echo "  - 📦 Microservices architecture"
    echo "  - 🚀 Async message processing"
    echo ""
}

# Main execution
main() {
    print_header "Personal Finance Management - Distributed System Demo"
    echo ""
    
    check_dependencies
    cleanup_existing
    start_services
    wait_for_services
    setup_database
    load_sample_data
    
    echo ""
    print_header "🎉 Demo Setup Complete!"
    echo ""
    
    show_services
    show_demo_guide
    
    print_status "To stop the demo: docker-compose down"
    print_status "To view logs: docker-compose logs -f [service-name]"
    print_status "To restart: ./setup_demo.sh"
}

# Run main function
main "$@"
