#!/usr/bin/env python
"""
Simple test script to verify the service architecture is working
"""

import os
import sys
import django
from datetime import date
from decimal import Decimal

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "financeapp.settings")
django.setup()

from django.contrib.auth.models import User
from finance.domain.entities import TransactionType, CryptoType
from finance.infrastructure.container import container


def test_transaction_service():
    """Test transaction service functionality"""
    print("Testing Transaction Service...")

    # Create a test user
    user, created = User.objects.get_or_create(
        username="testuser", defaults={"email": "test@example.com"}
    )

    # Create a test category
    from finance.models import Category

    category, created = Category.objects.get_or_create(
        user=user, name="Test Income", transaction_type="Income"
    )

    try:
        # Test registering a transaction
        register_service = container.register_transaction_service()
        transaction = register_service.execute(
            user_id=user.id,
            transaction_type=TransactionType.INCOME,
            amount=Decimal("1000.00"),
            category_id=category.id,
            transaction_date=date.today(),
        )

        print(
            f"✅ Transaction created: ID {transaction.id}, Amount: ${transaction.amount}"
        )

        # Test getting user transactions
        get_service = container.get_user_transactions_service()
        transactions = get_service.execute(user.id)

        print(f"✅ Retrieved {len(transactions)} transactions for user")

        return True

    except Exception as e:
        print(f"❌ Transaction service test failed: {e}")
        return False


def test_retirement_service():
    """Test retirement service functionality"""
    print("\nTesting Retirement Service...")

    user, created = User.objects.get_or_create(
        username="testuser", defaults={"email": "test@example.com"}
    )

    try:
        # Test creating a retirement goal
        create_service = container.create_retirement_goal_service()
        goal = create_service.execute(
            user_id=user.id,
            target_amount=Decimal("500000.00"),
            target_date=date(2050, 12, 31),
            monthly_contribution=Decimal("1000.00"),
            current_amount=Decimal("10000.00"),
        )

        print(
            f"✅ Retirement goal created: ID {goal.id}, Target: ${goal.target_amount}"
        )

        # Test adding a contribution
        add_service = container.add_retirement_contribution_service()
        contribution = add_service.execute(
            user_id=user.id,
            retirement_goal_id=goal.id,
            amount=Decimal("500.00"),
            contribution_date=date.today(),
            description="Test contribution",
        )

        print(
            f"✅ Retirement contribution added: ID {contribution.id}, Amount: ${contribution.amount}"
        )

        return True

    except Exception as e:
        print(f"❌ Retirement service test failed: {e}")
        return False


def test_crypto_service():
    """Test crypto service functionality"""
    print("\nTesting Crypto Service...")

    user, created = User.objects.get_or_create(
        username="testuser", defaults={"email": "test@example.com"}
    )

    try:
        # Test registering a crypto investment
        register_service = container.register_crypto_investment_service()
        investment = register_service.execute(
            user_id=user.id,
            crypto_type=CryptoType.BTC,
            amount_invested=Decimal("5000.00"),
            quantity=Decimal("0.1"),
            purchase_price=Decimal("50000.00"),
            purchase_date=date.today(),
        )

        print(
            f"✅ Crypto investment created: ID {investment.id}, Type: {investment.crypto_type.value}"
        )

        # Test getting portfolio summary
        summary_service = container.get_crypto_portfolio_summary_service()
        summary = summary_service.execute(user.id)

        print(f"✅ Portfolio summary: Total invested: ${summary['total_invested']}")

        return True

    except Exception as e:
        print(f"❌ Crypto service test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("🚀 Starting Service Architecture Tests\n")

    results = []
    results.append(test_transaction_service())
    results.append(test_retirement_service())
    results.append(test_crypto_service())

    print(f"\n📊 Test Results:")
    print(f"✅ Passed: {sum(results)}")
    print(f"❌ Failed: {len(results) - sum(results)}")

    if all(results):
        print("\n🎉 All tests passed! Service architecture is working correctly.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
