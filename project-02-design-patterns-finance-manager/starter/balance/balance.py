# balance.py

from balance.transaction_strategy import ExpenseStrategy, IncomeStrategy
from transaction.transaction_category import TransactionCategory


class Balance:
    """Singleton to track the balance."""

    _instance = None

    def __new__(cls):
        """Return the application's single balance manager instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the balance once, even when ``Balance()`` is repeated."""
        if getattr(self, "_initialized", False):
            return

        self._balance = 0.0
        self._observers = []
        self._transaction_strategies = {
            TransactionCategory.INCOME: IncomeStrategy(),
            TransactionCategory.EXPENSE: ExpenseStrategy(),
        }
        self._initialized = True

    @classmethod
    def get_instance(cls):
        """Return the single balance manager instance."""
        return cls()

    def register_observer(self, observer):
        """Register an observer to receive balance-change notifications."""
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        """Stop an observer from receiving balance-change notifications."""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, transaction):
        """Notify all registered observers about an applied transaction."""
        for observer in tuple(self._observers):
            observer.update(self, transaction)

    def register_transaction_strategy(self, category, strategy):
        """Set the calculation strategy used for a transaction category."""
        self._transaction_strategies[category] = strategy

    def reset(self):
        """Reset the net balance to zero."""
        self._balance = 0.0

    def add_income(self, amount):
        """Add income to the balance."""
        self._balance += amount

    def add_expense(self, amount):
        """Subtract expense from the balance."""
        self._balance -= amount

    def apply_transaction(self, transaction):
        """
        Apply a Transaction object to update the balance.

        Args:
            transaction (Transaction): The transaction to apply.
        """
        strategy = self._transaction_strategies.get(transaction.category)
        if strategy is None:
            raise ValueError(
                f"Unsupported transaction category: {transaction.category}"
            )

        self._balance = strategy.calculate(self._balance, transaction.amount)
        self.notify_observers(transaction)

    def get_balance(self):
        """Get the current net balance."""
        return self._balance

    def summary(self):
        """Return a summary string of the net balance."""
        return f"Net balance: {self._balance:.2f}"
    
