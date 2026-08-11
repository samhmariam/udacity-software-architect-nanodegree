"""Strategies for applying transaction amounts to a balance."""

from abc import ABC, abstractmethod


class TransactionStrategy(ABC):
    """Define how a transaction changes the current balance."""

    @abstractmethod
    def calculate(self, current_balance, amount):
        """Return the balance after applying ``amount``."""


class IncomeStrategy(TransactionStrategy):
    """Increase the balance by the transaction amount."""

    def calculate(self, current_balance, amount):
        return current_balance + amount


class ExpenseStrategy(TransactionStrategy):
    """Decrease the balance by the transaction amount."""

    def calculate(self, current_balance, amount):
        return current_balance - amount
