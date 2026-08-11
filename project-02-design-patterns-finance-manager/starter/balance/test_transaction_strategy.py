import unittest

from balance.balance import Balance
from balance.transaction_strategy import ExpenseStrategy, IncomeStrategy
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory


class TestTransactionStrategy(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()

    def test_income_strategy_adds_amount(self):
        strategy = IncomeStrategy()
        self.assertEqual(strategy.calculate(100, 25), 125)

    def test_expense_strategy_subtracts_amount(self):
        strategy = ExpenseStrategy()
        self.assertEqual(strategy.calculate(100, 25), 75)

    def test_balance_uses_strategy_for_transaction_category(self):
        self.balance.apply_transaction(
            Transaction(40, TransactionCategory.INCOME)
        )
        self.balance.apply_transaction(
            Transaction(15, TransactionCategory.EXPENSE)
        )
        self.assertEqual(self.balance.get_balance(), 25)

    def test_custom_strategy_can_be_registered(self):
        class FeeStrategy:
            def calculate(self, current_balance, amount):
                return current_balance - amount - 2

        fee_category = "fee"
        self.balance.register_transaction_strategy(fee_category, FeeStrategy())
        self.balance.apply_transaction(Transaction(10, fee_category))

        self.assertEqual(self.balance.get_balance(), -12)


if __name__ == "__main__":
    unittest.main()
