#!/usr/bin/env python
"""
Demo setup script for the Personal Finance Management System
This script creates sample data to demonstrate the new service-based architecture
"""

import os
import sys
import django
from datetime import date, timedelta
from decimal import Decimal

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "financeapp.settings")
django.setup()

from django.contrib.auth.models import User
from finance.models import Category
from finance.domain.entities import TransactionType, CryptoType
from finance.infrastructure.container import container


def create_demo_user():
    """Create a demo user with sample data"""
    print("Creating demo user...")

    # Create demo user
    user, created = User.objects.get_or_create(
        username="demo",
        defaults={
            "email": "demo@financeapp.com",
            "first_name": "Demo",
            "last_name": "User",
        },
    )

    if created:
        user.set_password("demo123")
        user.save()
        print("✅ Demo user created (username: demo, password: demo123)")
    else:
        print("✅ Demo user already exists")

    return user


def create_sample_categories(user):
    """Create sample income and expense categories"""
    print("Creating sample categories...")

    income_categories = [
        "Salary",
        "Freelance",
        "Investment Returns",
        "Side Business",
        "Bonus",
    ]

    expense_categories = [
        "Rent",
        "Groceries",
        "Transportation",
        "Utilities",
        "Entertainment",
        "Healthcare",
        "Insurance",
        "Dining Out",
        "Shopping",
        "Education",
    ]

    categories = []

    # Create income categories
    for name in income_categories:
        category, created = Category.objects.get_or_create(
            user=user, name=name, transaction_type="Income"
        )
        categories.append(category)

    # Create expense categories
    for name in expense_categories:
        category, created = Category.objects.get_or_create(
            user=user, name=name, transaction_type="Expense"
        )
        categories.append(category)

    print(f"✅ Created {len(categories)} categories")
    return categories


def create_sample_transactions(user, categories):
    """Create sample transactions using the service layer"""
    print("Creating sample transactions...")

    register_service = container.register_transaction_service()

    # Get categories by type
    income_categories = [c for c in categories if c.transaction_type == "Income"]
    expense_categories = [c for c in categories if c.transaction_type == "Expense"]

    transactions_created = 0

    # Create transactions for the last 6 months
    for month_offset in range(6):
        transaction_date = date.today() - timedelta(days=30 * month_offset)

        # Monthly salary
        salary_category = next(
            (c for c in income_categories if c.name == "Salary"), income_categories[0]
        )
        register_service.execute(
            user_id=user.id,
            transaction_type=TransactionType.INCOME,
            amount=Decimal("5000.00"),
            category_id=salary_category.id,
            transaction_date=transaction_date,
        )
        transactions_created += 1

        # Some freelance income
        if month_offset < 3:  # Only last 3 months
            freelance_category = next(
                (c for c in income_categories if c.name == "Freelance"),
                income_categories[1],
            )
            register_service.execute(
                user_id=user.id,
                transaction_type=TransactionType.INCOME,
                amount=Decimal("1200.00"),
                category_id=freelance_category.id,
                transaction_date=transaction_date,
            )
            transactions_created += 1

        # Monthly expenses
        monthly_expenses = [
            ("Rent", "1500.00"),
            ("Groceries", "400.00"),
            ("Transportation", "200.00"),
            ("Utilities", "150.00"),
            ("Insurance", "300.00"),
            ("Dining Out", "250.00"),
            ("Entertainment", "100.00"),
        ]

        for expense_name, amount in monthly_expenses:
            expense_category = next(
                (c for c in expense_categories if c.name == expense_name),
                expense_categories[0],
            )
            register_service.execute(
                user_id=user.id,
                transaction_type=TransactionType.EXPENSE,
                amount=Decimal(amount),
                category_id=expense_category.id,
                transaction_date=transaction_date,
            )
            transactions_created += 1

    print(f"✅ Created {transactions_created} sample transactions")


def create_sample_retirement_goals(user):
    """Create sample retirement goals and contributions"""
    print("Creating sample retirement data...")

    # Create retirement goal
    create_goal_service = container.create_retirement_goal_service()
    goal = create_goal_service.execute(
        user_id=user.id,
        target_amount=Decimal("1000000.00"),
        target_date=date(2055, 12, 31),
        monthly_contribution=Decimal("800.00"),
        current_amount=Decimal("25000.00"),
    )

    # Add some contributions
    add_contribution_service = container.add_retirement_contribution_service()

    contributions = [
        (Decimal("800.00"), date.today() - timedelta(days=30), "Monthly contribution"),
        (Decimal("800.00"), date.today() - timedelta(days=60), "Monthly contribution"),
        (Decimal("1500.00"), date.today() - timedelta(days=90), "Bonus contribution"),
        (Decimal("800.00"), date.today() - timedelta(days=120), "Monthly contribution"),
    ]

    for amount, contrib_date, description in contributions:
        add_contribution_service.execute(
            user_id=user.id,
            retirement_goal_id=goal.id,
            amount=amount,
            contribution_date=contrib_date,
            description=description,
        )

    print(f"✅ Created retirement goal with target ${goal.target_amount}")


def create_sample_crypto_investments(user):
    """Create sample crypto investments"""
    print("Creating sample crypto investments...")

    register_service = container.register_crypto_investment_service()

    # BTC investment
    btc_investment = register_service.execute(
        user_id=user.id,
        crypto_type=CryptoType.BTC,
        amount_invested=Decimal("10000.00"),
        quantity=Decimal("0.25"),
        purchase_price=Decimal("40000.00"),
        purchase_date=date.today() - timedelta(days=180),
    )

    # ETH investment
    eth_investment = register_service.execute(
        user_id=user.id,
        crypto_type=CryptoType.ETH,
        amount_invested=Decimal("5000.00"),
        quantity=Decimal("2.0"),
        purchase_price=Decimal("2500.00"),
        purchase_date=date.today() - timedelta(days=120),
    )

    # Update prices to simulate current market values
    update_service = container.update_crypto_price_service()

    # Update BTC price (simulate some gains)
    update_service.execute(btc_investment.id, Decimal("45000.00"))

    # Update ETH price (simulate some gains)
    update_service.execute(eth_investment.id, Decimal("2800.00"))

    print("✅ Created sample crypto investments with current prices")


def main():
    """Setup demo data"""
    print("🚀 Setting up Personal Finance Management Demo\n")

    try:
        # Create demo user
        user = create_demo_user()

        # Create sample categories
        categories = create_sample_categories(user)

        # Create sample transactions
        create_sample_transactions(user, categories)

        # Create retirement data
        create_sample_retirement_goals(user)

        # Create crypto investments
        create_sample_crypto_investments(user)

        print("\n🎉 Demo setup completed successfully!")
        print("\n📋 Demo Access Information:")
        print("   URL: http://localhost:8000/service/dashboard/")
        print("   Username: demo")
        print("   Password: demo123")
        print("\n🔗 Available Features:")
        print("   • Dashboard: http://localhost:8000/service/dashboard/")
        print("   • Retirement Planning: http://localhost:8000/service/retirement/")
        print("   • Crypto Investments: http://localhost:8000/service/crypto/")
        print("   • Add Transactions: Income/Expense forms")
        print("   • Reports & Forecasting: Original features still available")

        return 0

    except Exception as e:
        print(f"❌ Demo setup failed: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
