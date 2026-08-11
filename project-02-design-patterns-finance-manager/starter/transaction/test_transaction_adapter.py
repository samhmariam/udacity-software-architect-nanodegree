import unittest
from transaction.external_income_transaction import ExternalFreelanceIncome
from transaction.transaction_adapter import TransactionAdapter
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory

class TestTransactionAdapter(unittest.TestCase):

    def test_adapter_converts_freelance_income(self):
        ext_txn = ExternalFreelanceIncome(500, "INV-12345", "Website development")
        adapter = TransactionAdapter(ext_txn)
        txn = adapter.to_transaction()
        self.assertEqual(txn, Transaction(500, TransactionCategory.INCOME))

    def test_adapter_preserves_external_amount(self):
        ext_txn = ExternalFreelanceIncome(725.50, "INV-2", "API design")
        txn = TransactionAdapter(ext_txn).to_transaction()

        self.assertEqual(txn.amount, 725.50)

    def test_adapter_always_creates_income_transaction(self):
        ext_txn = ExternalFreelanceIncome(10, "INV-3", "Consulting")
        txn = TransactionAdapter(ext_txn).to_transaction()

        self.assertIs(txn.category, TransactionCategory.INCOME)

if __name__ == "__main__":
    unittest.main()
