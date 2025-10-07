from dependency_injector import containers, providers
from finance.interfaces.message_bus import MessageBus
from finance.infrastructure.kafka_message_bus import KafkaMessageBus
from finance.interfaces.repositories import (
    TransactionRepository,
    CategoryRepository,
    BudgetRepository,
    RetirementGoalRepository,
    RetirementContributionRepository,
    CryptoInvestmentRepository,
)
from finance.repositories.django_repositories import (
    DjangoTransactionRepository,
    DjangoCategoryRepository,
    DjangoBudgetRepository,
    DjangoRetirementGoalRepository,
    DjangoRetirementContributionRepository,
    DjangoCryptoInvestmentRepository,
)
from finance.services.transaction_services import (
    RegisterTransactionService,
    GetUserTransactionsService,
    UpdateTransactionService,
    DeleteTransactionService,
)
from finance.services.retirement_services import (
    CreateRetirementGoalService,
    GetUserRetirementGoalsService,
    AddRetirementContributionService,
    GetRetirementContributionsService,
    GetGoalContributionsService,
    UpdateRetirementGoalService,
)
from finance.services.crypto_services import (
    RegisterCryptoInvestmentService,
    GetUserCryptoInvestmentsService,
    GetCryptoInvestmentsByTypeService,
    UpdateCryptoPriceService,
    UpdateAllCryptoPricesService,
    GetCryptoPortfolioSummaryService,
    SellCryptoInvestmentService,
)


class Container(containers.DeclarativeContainer):
    """Dependency injection container"""

    # Configuration
    config = providers.Configuration()

    # Infrastructure
    message_bus: providers.Provider[MessageBus] = providers.Singleton(
        KafkaMessageBus,
        bootstrap_servers=config.kafka.bootstrap_servers.as_(str),
    )

    # Repositories
    transaction_repository: providers.Provider[TransactionRepository] = (
        providers.Factory(DjangoTransactionRepository)
    )

    category_repository: providers.Provider[CategoryRepository] = providers.Factory(
        DjangoCategoryRepository
    )

    budget_repository: providers.Provider[BudgetRepository] = providers.Factory(
        DjangoBudgetRepository
    )

    retirement_goal_repository: providers.Provider[RetirementGoalRepository] = (
        providers.Factory(DjangoRetirementGoalRepository)
    )

    retirement_contribution_repository: providers.Provider[
        RetirementContributionRepository
    ] = providers.Factory(DjangoRetirementContributionRepository)

    crypto_investment_repository: providers.Provider[CryptoInvestmentRepository] = (
        providers.Factory(DjangoCryptoInvestmentRepository)
    )

    # Transaction Services
    register_transaction_service = providers.Factory(
        RegisterTransactionService,
        transaction_repository=transaction_repository,
        category_repository=category_repository,
        message_bus=message_bus,
    )

    get_user_transactions_service = providers.Factory(
        GetUserTransactionsService,
        transaction_repository=transaction_repository,
    )

    update_transaction_service = providers.Factory(
        UpdateTransactionService,
        transaction_repository=transaction_repository,
        category_repository=category_repository,
        message_bus=message_bus,
    )

    delete_transaction_service = providers.Factory(
        DeleteTransactionService,
        transaction_repository=transaction_repository,
        message_bus=message_bus,
    )

    # Retirement Services
    create_retirement_goal_service = providers.Factory(
        CreateRetirementGoalService,
        retirement_goal_repository=retirement_goal_repository,
        message_bus=message_bus,
    )

    get_user_retirement_goals_service = providers.Factory(
        GetUserRetirementGoalsService,
        retirement_goal_repository=retirement_goal_repository,
    )

    add_retirement_contribution_service = providers.Factory(
        AddRetirementContributionService,
        retirement_goal_repository=retirement_goal_repository,
        retirement_contribution_repository=retirement_contribution_repository,
        message_bus=message_bus,
    )

    get_retirement_contributions_service = providers.Factory(
        GetRetirementContributionsService,
        retirement_contribution_repository=retirement_contribution_repository,
    )

    get_goal_contributions_service = providers.Factory(
        GetGoalContributionsService,
        retirement_goal_repository=retirement_goal_repository,
        retirement_contribution_repository=retirement_contribution_repository,
    )

    update_retirement_goal_service = providers.Factory(
        UpdateRetirementGoalService,
        retirement_goal_repository=retirement_goal_repository,
        message_bus=message_bus,
    )

    # Crypto Services
    register_crypto_investment_service = providers.Factory(
        RegisterCryptoInvestmentService,
        crypto_investment_repository=crypto_investment_repository,
        message_bus=message_bus,
    )

    get_user_crypto_investments_service = providers.Factory(
        GetUserCryptoInvestmentsService,
        crypto_investment_repository=crypto_investment_repository,
    )

    get_crypto_investments_by_type_service = providers.Factory(
        GetCryptoInvestmentsByTypeService,
        crypto_investment_repository=crypto_investment_repository,
    )

    update_crypto_price_service = providers.Factory(
        UpdateCryptoPriceService,
        crypto_investment_repository=crypto_investment_repository,
        message_bus=message_bus,
    )

    update_all_crypto_prices_service = providers.Factory(
        UpdateAllCryptoPricesService,
        crypto_investment_repository=crypto_investment_repository,
        message_bus=message_bus,
    )

    get_crypto_portfolio_summary_service = providers.Factory(
        GetCryptoPortfolioSummaryService,
        crypto_investment_repository=crypto_investment_repository,
    )

    sell_crypto_investment_service = providers.Factory(
        SellCryptoInvestmentService,
        crypto_investment_repository=crypto_investment_repository,
        message_bus=message_bus,
    )


# Global container instance
container = Container()

# Configure with default values
container.config.kafka.bootstrap_servers.from_value("localhost:9092")
