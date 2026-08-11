import unittest
from balance.balance import Balance
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory

class TestBalance(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()

    def test_initial_balance(self):
        self.assertEqual(self.balance.get_balance(), 0.0)

    def test_singleton_instance(self):
        balance1 = Balance.get_instance()
        balance2 = Balance.get_instance()
        self.assertIs(balance1, balance2)

    def test_direct_construction_returns_singleton(self):
        self.assertIs(Balance(), Balance.get_instance())

    def test_repeated_access_preserves_balance(self):
        self.balance.add_income(25)
        self.assertEqual(Balance.get_instance().get_balance(), 25)

    def test_add_income(self):
        self.balance.add_income(100)
        self.assertEqual(self.balance.get_balance(), 100)

    def test_add_expense(self):
        self.balance.add_expense(40)
        self.assertEqual(self.balance.get_balance(), -40)

    def test_apply_transaction_income(self):
        t = Transaction(150, TransactionCategory.INCOME)
        self.balance.apply_transaction(t)
        self.assertEqual(self.balance.get_balance(), 150)

    def test_apply_transaction_expense(self):
        t = Transaction(60, TransactionCategory.EXPENSE)
        self.balance.apply_transaction(t)
        self.assertEqual(self.balance.get_balance(), -60)

    def test_apply_transaction_invalid_category(self):
        class FakeCategory:
            pass
        t = Transaction(100, FakeCategory())
        with self.assertRaises(ValueError):
            self.balance.apply_transaction(t)

    def test_reset(self):
        self.balance.add_income(100)
        self.balance.add_expense(50)
        self.balance.reset()
        self.assertEqual(self.balance.get_balance(), 0.0)

    def test_summary_formats_balance_to_two_decimal_places(self):
        self.balance.add_income(12.5)
        self.assertEqual(self.balance.summary(), "Net balance: 12.50")

if __name__ == "__main__":
    unittest.main()
