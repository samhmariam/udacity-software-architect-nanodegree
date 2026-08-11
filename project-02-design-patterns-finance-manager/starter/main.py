"""This module serves as the entry point for the program."""
from balance.balance import Balance
from balance.balance_observer import LowBalanceAlertObserver, PrintBalanceObserver
from transaction.external_income_transaction import ExternalFreelanceIncome
from transaction.transaction import Transaction
from transaction.transaction_adapter import TransactionAdapter
from transaction.transaction_category import TransactionCategory


def main():
    print("Adding transactions...")

    balance = Balance.get_instance()
    balance.reset()
    balance.register_observer(PrintBalanceObserver())
    balance.register_observer(LowBalanceAlertObserver(threshold=100))

    # Create standard transactions
    transactions = [
        Transaction(100, TransactionCategory.INCOME),
        Transaction(50, TransactionCategory.EXPENSE),
        Transaction(200, TransactionCategory.INCOME),
        Transaction(75, TransactionCategory.EXPENSE),
    ]

    # Create an external income transaction (via Adapter pattern)
    freelance_income = ExternalFreelanceIncome(
        1200,
        "INV-98765",
        "Mobile App Project",
    )
    adapter = TransactionAdapter(freelance_income)
    adapted_transaction = adapter.to_transaction()

    all_transactions = transactions + [adapted_transaction]

    for transaction in all_transactions:
        balance.apply_transaction(transaction)

    print(f"Final {balance.summary().lower()}")


if __name__ == "__main__":
    main()
