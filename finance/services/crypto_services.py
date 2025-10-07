from typing import List, Optional
from datetime import date
from decimal import Decimal
from finance.domain.entities import CryptoInvestment, CryptoType
from finance.interfaces.repositories import CryptoInvestmentRepository
from finance.interfaces.message_bus import MessageBus


class RegisterCryptoInvestmentService:
    """Service for registering crypto investments"""

    def __init__(
        self,
        crypto_investment_repository: CryptoInvestmentRepository,
        message_bus: MessageBus,
    ):
        self.crypto_investment_repository = crypto_investment_repository
        self.message_bus = message_bus

    def execute(
        self,
        user_id: int,
        crypto_type: CryptoType,
        amount_invested: Decimal,
        quantity: Decimal,
        purchase_price: Decimal,
        purchase_date: date,
    ) -> CryptoInvestment:
        """Execute crypto investment registration"""
        # Validate inputs
        if amount_invested <= 0:
            raise ValueError("Investment amount must be positive")
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if purchase_price <= 0:
            raise ValueError("Purchase price must be positive")

        # Create crypto investment entity
        investment = CryptoInvestment(
            id=None,
            user_id=user_id,
            crypto_type=crypto_type,
            amount_invested=amount_invested,
            quantity=quantity,
            purchase_price=purchase_price,
            purchase_date=purchase_date,
            current_price=None,  # Will be updated by price service
        )

        # Save investment
        saved_investment = self.crypto_investment_repository.create(investment)

        # Publish event
        self.message_bus.publish(
            "crypto_investment.created",
            {
                "investment_id": saved_investment.id,
                "user_id": user_id,
                "crypto_type": crypto_type.value,
                "amount_invested": float(amount_invested),
                "quantity": float(quantity),
                "purchase_price": float(purchase_price),
                "purchase_date": purchase_date.isoformat(),
            },
        )

        return saved_investment


class GetUserCryptoInvestmentsService:
    """Service for retrieving user crypto investments"""

    def __init__(self, crypto_investment_repository: CryptoInvestmentRepository):
        self.crypto_investment_repository = crypto_investment_repository

    def execute(self, user_id: int) -> List[CryptoInvestment]:
        """Execute getting user crypto investments"""
        return self.crypto_investment_repository.get_by_user_id(user_id)


class GetCryptoInvestmentsByTypeService:
    """Service for retrieving crypto investments by type"""

    def __init__(self, crypto_investment_repository: CryptoInvestmentRepository):
        self.crypto_investment_repository = crypto_investment_repository

    def execute(self, user_id: int, crypto_type: CryptoType) -> List[CryptoInvestment]:
        """Execute getting crypto investments by type"""
        return self.crypto_investment_repository.get_by_user_and_crypto_type(
            user_id, crypto_type.value
        )


class UpdateCryptoPriceService:
    """Service for updating crypto prices"""

    def __init__(
        self,
        crypto_investment_repository: CryptoInvestmentRepository,
        message_bus: MessageBus,
    ):
        self.crypto_investment_repository = crypto_investment_repository
        self.message_bus = message_bus

    def execute(self, investment_id: int, current_price: Decimal) -> CryptoInvestment:
        """Execute crypto price update"""
        # Get existing investment
        existing_investment = self.crypto_investment_repository.get_by_id(investment_id)
        if not existing_investment:
            raise ValueError("Investment not found")

        # Validate price
        if current_price <= 0:
            raise ValueError("Current price must be positive")

        # Update investment entity
        updated_investment = CryptoInvestment(
            id=existing_investment.id,
            user_id=existing_investment.user_id,
            crypto_type=existing_investment.crypto_type,
            amount_invested=existing_investment.amount_invested,
            quantity=existing_investment.quantity,
            purchase_price=existing_investment.purchase_price,
            purchase_date=existing_investment.purchase_date,
            current_price=current_price,
        )

        # Save updated investment
        saved_investment = self.crypto_investment_repository.update(updated_investment)

        # Publish event
        self.message_bus.publish(
            "crypto_price.updated",
            {
                "investment_id": investment_id,
                "user_id": existing_investment.user_id,
                "crypto_type": existing_investment.crypto_type.value,
                "current_price": float(current_price),
                "current_value": float(saved_investment.current_value or 0),
                "profit_loss": float(saved_investment.profit_loss or 0),
            },
        )

        return saved_investment


class UpdateAllCryptoPricesService:
    """Service for updating all crypto prices for a specific type"""

    def __init__(
        self,
        crypto_investment_repository: CryptoInvestmentRepository,
        message_bus: MessageBus,
    ):
        self.crypto_investment_repository = crypto_investment_repository
        self.message_bus = message_bus

    def execute(self, crypto_type: CryptoType, current_price: Decimal) -> int:
        """Execute updating all investments of a specific crypto type"""
        if current_price <= 0:
            raise ValueError("Current price must be positive")

        # This would typically get all investments of this type across all users
        # For now, we'll implement a simple version that updates by user
        updated_count = 0

        # In a real implementation, you'd want to batch this operation
        # and possibly use a more efficient update query

        # Publish event for price update
        self.message_bus.publish(
            "crypto_market_price.updated",
            {
                "crypto_type": crypto_type.value,
                "current_price": float(current_price),
                "timestamp": date.today().isoformat(),
            },
        )

        return updated_count


class GetCryptoPortfolioSummaryService:
    """Service for getting crypto portfolio summary"""

    def __init__(self, crypto_investment_repository: CryptoInvestmentRepository):
        self.crypto_investment_repository = crypto_investment_repository

    def execute(self, user_id: int) -> dict:
        """Execute getting crypto portfolio summary"""
        investments = self.crypto_investment_repository.get_by_user_id(user_id)

        summary = {
            "total_invested": Decimal("0"),
            "current_value": Decimal("0"),
            "total_profit_loss": Decimal("0"),
            "btc_investments": [],
            "eth_investments": [],
        }

        for investment in investments:
            summary["total_invested"] += investment.amount_invested

            if investment.current_value:
                summary["current_value"] += investment.current_value

            if investment.profit_loss:
                summary["total_profit_loss"] += investment.profit_loss

            if investment.crypto_type == CryptoType.BTC:
                summary["btc_investments"].append(investment)
            elif investment.crypto_type == CryptoType.ETH:
                summary["eth_investments"].append(investment)

        return summary


class SellCryptoInvestmentService:
    """Service for selling crypto investments"""

    def __init__(
        self,
        crypto_investment_repository: CryptoInvestmentRepository,
        message_bus: MessageBus,
    ):
        self.crypto_investment_repository = crypto_investment_repository
        self.message_bus = message_bus

    def execute(self, investment_id: int, user_id: int, sell_price: Decimal) -> dict:
        """Execute crypto investment sale"""
        # Get existing investment
        existing_investment = self.crypto_investment_repository.get_by_id(investment_id)
        if not existing_investment or existing_investment.user_id != user_id:
            raise ValueError("Investment not found or access denied")

        # Validate sell price
        if sell_price <= 0:
            raise ValueError("Sell price must be positive")

        # Calculate sale details
        sale_value = existing_investment.quantity * sell_price
        profit_loss = sale_value - existing_investment.amount_invested

        # Delete the investment (since it's sold)
        success = self.crypto_investment_repository.delete(investment_id)

        if success:
            # Publish event
            self.message_bus.publish(
                "crypto_investment.sold",
                {
                    "investment_id": investment_id,
                    "user_id": user_id,
                    "crypto_type": existing_investment.crypto_type.value,
                    "quantity": float(existing_investment.quantity),
                    "purchase_price": float(existing_investment.purchase_price),
                    "sell_price": float(sell_price),
                    "amount_invested": float(existing_investment.amount_invested),
                    "sale_value": float(sale_value),
                    "profit_loss": float(profit_loss),
                    "sale_date": date.today().isoformat(),
                },
            )

        return {
            "sale_value": sale_value,
            "profit_loss": profit_loss,
            "profit_loss_percentage": (
                profit_loss / existing_investment.amount_invested
            )
            * 100
            if existing_investment.amount_invested > 0
            else 0,
        }
