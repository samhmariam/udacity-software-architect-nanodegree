import unittest
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory

class TestTransaction(unittest.TestCase):

    def test_transaction_creation(self):
        t = Transaction(100, TransactionCategory.EXPENSE)
        self.assertEqual(t.amount, 100)
        self.assertEqual(t.category, TransactionCategory.EXPENSE)

    def test_transaction_str(self):
        t = Transaction(50, TransactionCategory.INCOME)
        self.assertEqual(
            str(t),
            "Transaction($50, category='TransactionCategory.INCOME')",
        )

    def test_transaction_equality(self):
        t1 = Transaction(20, TransactionCategory.EXPENSE)
        t2 = Transaction(20, TransactionCategory.EXPENSE)
        t3 = Transaction(30, TransactionCategory.EXPENSE)
        self.assertEqual(t1, t2)
        self.assertNotEqual(t1, t3)

    def test_transactions_with_different_categories_are_not_equal(self):
        income = Transaction(20, TransactionCategory.INCOME)
        expense = Transaction(20, TransactionCategory.EXPENSE)
        self.assertNotEqual(income, expense)

    def test_transaction_is_not_equal_to_unrelated_type(self):
        self.assertNotEqual(Transaction(20, TransactionCategory.INCOME), 20)

    def test_transaction_category_is_an_enum(self):
        self.assertEqual(TransactionCategory.INCOME.value, "Income")
        self.assertEqual(TransactionCategory.EXPENSE.value, "Expense")

if __name__ == "__main__":
    unittest.main()
