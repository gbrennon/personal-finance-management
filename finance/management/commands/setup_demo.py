from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from datetime import date, timedelta
from decimal import Decimal
import random

from finance.models import Category, Transaction, Budget
from investments.models import InvestmentType, Investment, InvestmentTransaction
from retirement.models import RetirementAccount, RetirementContribution, RetirementGoal
from banks.models import BankInstitution, BankAccount, BankTransaction


class Command(BaseCommand):
    help = "Set up demo data for the personal finance application"

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            type=str,
            default="demo",
            help="Username for the demo user (default: demo)",
        )
        parser.add_argument(
            "--password",
            type=str,
            default="demo123",
            help="Password for the demo user (default: demo123)",
        )

    def handle(self, *args, **options):
        username = options["username"]
        password = options["password"]

        self.stdout.write(self.style.SUCCESS("Setting up demo data..."))

        # Create or get demo user
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": f"{username}@example.com",
                "first_name": "Demo",
                "last_name": "User",
            },
        )
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(f"Created demo user: {username}")
        else:
            self.stdout.write(f"Using existing user: {username}")

        # Setup Finance data
        self.setup_finance_data(user)

        # Setup Investment data
        self.setup_investment_data(user)

        # Setup Retirement data
        self.setup_retirement_data(user)

        # Setup Bank data
        self.setup_bank_data(user)

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDemo setup complete!\n"
                f"Login credentials:\n"
                f"Username: {username}\n"
                f"Password: {password}\n"
                f"\nYou can now explore all the features of the application."
            )
        )

    def setup_finance_data(self, user):
        self.stdout.write("Setting up finance data...")

        # Create categories
        income_categories = [
            "Salary",
            "Freelance",
            "Investment Income",
            "Bonus",
            "Other Income",
        ]
        expense_categories = [
            "Rent/Mortgage",
            "Groceries",
            "Utilities",
            "Transportation",
            "Entertainment",
            "Healthcare",
            "Insurance",
            "Dining Out",
            "Shopping",
        ]

        for cat_name in income_categories:
            Category.objects.get_or_create(
                user=user, name=cat_name, transaction_type="Income"
            )

        for cat_name in expense_categories:
            Category.objects.get_or_create(
                user=user, name=cat_name, transaction_type="Expense"
            )

        # Create sample transactions
        categories = Category.objects.filter(user=user)

        # Income transactions
        income_cats = categories.filter(transaction_type="Income")
        for i in range(12):  # 12 months of data
            transaction_date = date.today() - timedelta(days=30 * i)
            for cat in income_cats[:2]:  # Use first 2 income categories
                amount = random.uniform(3000, 8000)
                Transaction.objects.create(
                    user=user,
                    transaction_type="Income",
                    amount=Decimal(str(round(amount, 2))),
                    category=cat,
                    date=transaction_date,
                )

        # Expense transactions
        expense_cats = categories.filter(transaction_type="Expense")
        for i in range(90):  # 90 days of expenses
            transaction_date = date.today() - timedelta(days=i)
            cat = random.choice(expense_cats)
            amount = random.uniform(20, 500)
            Transaction.objects.create(
                user=user,
                transaction_type="Expense",
                amount=Decimal(str(round(amount, 2))),
                category=cat,
                date=transaction_date,
            )

        # Create budget
        Budget.objects.get_or_create(
            user=user,
            month=date.today().month,
            year=date.today().year,
            defaults={"amount": Decimal("4500.00")},
        )

    def setup_investment_data(self, user):
        self.stdout.write("Setting up investment data...")

        # Create investment types
        investment_types = [
            ("Stocks", "Individual company stocks"),
            ("ETF", "Exchange Traded Funds"),
            ("Mutual Fund", "Mutual Funds"),
            ("Cryptocurrency", "Digital currencies"),
            ("Bonds", "Government and corporate bonds"),
        ]

        for name, desc in investment_types:
            InvestmentType.objects.get_or_create(
                name=name, defaults={"description": desc}
            )

        # Create sample investments
        stock_type = InvestmentType.objects.get(name="Stocks")
        etf_type = InvestmentType.objects.get(name="ETF")
        crypto_type = InvestmentType.objects.get(name="Cryptocurrency")

        investments_data = [
            ("Apple Inc.", "AAPL", stock_type, 150.00, 10),
            ("Microsoft Corp.", "MSFT", stock_type, 280.00, 5),
            ("SPDR S&P 500 ETF", "SPY", etf_type, 420.00, 25),
            ("Vanguard Total Stock Market ETF", "VTI", etf_type, 200.00, 15),
            ("Bitcoin", "BTC", crypto_type, 45000.00, 0.5),
        ]

        for name, symbol, inv_type, price, quantity in investments_data:
            investment = Investment.objects.create(
                user=user,
                name=name,
                symbol=symbol,
                investment_type=inv_type,
                purchase_date=date.today() - timedelta(days=random.randint(30, 365)),
                purchase_price=Decimal(str(price)),
                quantity=Decimal(str(quantity)),
                current_price=Decimal(str(price * random.uniform(0.9, 1.2))),
                notes=f"Demo investment in {name}",
            )

            # Create some transactions
            InvestmentTransaction.objects.create(
                user=user,
                investment=investment,
                transaction_type="BUY",
                quantity=Decimal(str(quantity)),
                price_per_unit=Decimal(str(price)),
                transaction_date=investment.purchase_date,
                fees=Decimal("9.99"),
            )

    def setup_retirement_data(self, user):
        self.stdout.write("Setting up retirement data...")

        # Create retirement accounts
        accounts_data = [
            ("401(k) - Current Employer", "401K", "Fidelity", 45000.00),
            ("Traditional IRA", "IRA", "Vanguard", 25000.00),
            ("Roth IRA", "ROTH_IRA", "Charles Schwab", 15000.00),
        ]

        for name, acc_type, provider, balance in accounts_data:
            account, created = RetirementAccount.objects.get_or_create(
                user=user,
                account_name=name,
                defaults={
                    "account_type": acc_type,
                    "provider": provider,
                    "current_balance": Decimal(str(balance)),
                    "employer_match_rate": Decimal("50.00")
                    if acc_type == "401K"
                    else None,
                },
            )

            # Create some contributions
            for i in range(6):  # 6 months of contributions
                contrib_date = date.today() - timedelta(days=30 * i)
                amount = random.uniform(500, 1500)
                RetirementContribution.objects.create(
                    user=user,
                    account=account,
                    contribution_type="EMPLOYEE",
                    amount=Decimal(str(round(amount, 2))),
                    contribution_date=contrib_date,
                    tax_year=contrib_date.year,
                )

        # Create retirement goal
        RetirementGoal.objects.get_or_create(
            user=user,
            defaults={
                "target_retirement_age": 65,
                "target_retirement_amount": Decimal("1000000.00"),
                "current_age": 35,
                "annual_income": Decimal("75000.00"),
                "expected_annual_return": Decimal("7.00"),
                "inflation_rate": Decimal("3.00"),
                "retirement_income_replacement": Decimal("80.00"),
            },
        )

    def setup_bank_data(self, user):
        self.stdout.write("Setting up bank data...")

        # Create bank institutions
        institutions_data = [
            ("Chase Bank", "021000021", "https://chase.com", "1-800-CHASE"),
            (
                "Bank of America",
                "026009593",
                "https://bankofamerica.com",
                "1-800-432-1000",
            ),
            ("Wells Fargo", "121000248", "https://wellsfargo.com", "1-800-869-3557"),
            ("Capital One", "031176110", "https://capitalone.com", "1-800-655-2265"),
        ]

        for name, routing, website, phone in institutions_data:
            BankInstitution.objects.get_or_create(
                name=name,
                defaults={
                    "routing_number": routing,
                    "website": website,
                    "phone": phone,
                },
            )

        # Create bank accounts
        chase = BankInstitution.objects.get(name="Chase Bank")
        bofa = BankInstitution.objects.get(name="Bank of America")
        wells = BankInstitution.objects.get(name="Wells Fargo")
        capital_one = BankInstitution.objects.get(name="Capital One")

        accounts_data = [
            ("Primary Checking", "CHECKING", chase, 2500.00, 2500.00, None),
            ("High Yield Savings", "SAVINGS", bofa, 15000.00, 15000.00, None),
            ("Emergency Fund", "SAVINGS", wells, 10000.00, 10000.00, None),
            ("Credit Card", "CREDIT_CARD", capital_one, -850.00, 1150.00, 2000.00),
        ]

        for (
            name,
            acc_type,
            institution,
            balance,
            available,
            credit_limit,
        ) in accounts_data:
            account = BankAccount.objects.create(
                user=user,
                institution=institution,
                account_name=name,
                account_type=acc_type,
                account_number=f"****{random.randint(1000, 9999)}",
                current_balance=Decimal(str(balance)),
                available_balance=Decimal(str(available)) if available else None,
                credit_limit=Decimal(str(credit_limit)) if credit_limit else None,
                interest_rate=Decimal("0.50") if acc_type == "SAVINGS" else None,
                monthly_fee=Decimal("0.00"),
            )

            # Create sample transactions
            for i in range(30):  # 30 days of transactions
                trans_date = date.today() - timedelta(days=i)

                if acc_type in ["CHECKING", "SAVINGS"]:
                    trans_types = ["DEPOSIT", "WITHDRAWAL", "TRANSFER", "PAYMENT"]
                    trans_type = random.choice(trans_types)
                    amount = random.uniform(50, 500)
                    if trans_type in ["WITHDRAWAL", "PAYMENT"]:
                        amount = -amount
                else:  # Credit card
                    trans_types = ["PAYMENT", "DEBIT"]
                    trans_type = random.choice(trans_types)
                    amount = random.uniform(20, 200)
                    if trans_type == "PAYMENT":
                        amount = amount  # Positive for payments
                    else:
                        amount = -amount  # Negative for purchases

                descriptions = [
                    "Grocery Store Purchase",
                    "Gas Station",
                    "Online Purchase",
                    "Restaurant",
                    "ATM Withdrawal",
                    "Direct Deposit",
                    "Utility Payment",
                    "Insurance Payment",
                    "Subscription Service",
                    "Coffee Shop",
                ]

                BankTransaction.objects.create(
                    user=user,
                    account=account,
                    transaction_type=trans_type,
                    amount=Decimal(str(round(amount, 2))),
                    description=random.choice(descriptions),
                    transaction_date=trans_date,
                    status="CLEARED",
                    category=random.choice(
                        [
                            "Food",
                            "Transportation",
                            "Utilities",
                            "Entertainment",
                            "Other",
                        ]
                    ),
                )
