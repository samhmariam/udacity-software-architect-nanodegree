import io
import unittest
from contextlib import redirect_stdout
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from balance.balance import Balance
from balance.balance_observer import LowBalanceAlertObserver, PrintBalanceObserver

class TestLowBalanceAlertObserver(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()
        self.observers = []

    def tearDown(self):
        for observer in self.observers:
            self.balance.remove_observer(observer)

    def register(self, observer):
        self.observers.append(observer)
        self.balance.register_observer(observer)
        return observer

    def test_alert_triggers_on_low_balance(self):
        observer = self.register(LowBalanceAlertObserver(threshold=50))

        self.balance.apply_transaction(Transaction(100, TransactionCategory.INCOME))
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(Transaction(60, TransactionCategory.EXPENSE))
        self.assertTrue(observer.alert_triggered)

        self.balance.apply_transaction(Transaction(100, TransactionCategory.INCOME))
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(Transaction(60, TransactionCategory.EXPENSE))
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(Transaction(60, TransactionCategory.EXPENSE))
        self.assertTrue(observer.alert_triggered)

    def test_observer_is_not_registered_twice(self):
        class CountingObserver:
            def __init__(self):
                self.updates = 0

            def update(self, balance, transaction):
                self.updates += 1

        observer = self.register(CountingObserver())
        self.balance.register_observer(observer)
        self.balance.apply_transaction(Transaction(10, TransactionCategory.INCOME))

        self.assertEqual(observer.updates, 1)

    def test_removed_observer_is_not_notified(self):
        class CountingObserver:
            updates = 0

            def update(self, balance, transaction):
                self.updates += 1

        observer = self.register(CountingObserver())
        self.balance.remove_observer(observer)
        self.balance.apply_transaction(Transaction(10, TransactionCategory.INCOME))

        self.assertEqual(observer.updates, 0)

    def test_print_observer_reports_balance_change(self):
        observer = self.register(PrintBalanceObserver())
        output = io.StringIO()

        with redirect_stdout(output):
            self.balance.apply_transaction(
                Transaction(30, TransactionCategory.INCOME)
            )

        self.assertIn("Balance updated: Net balance: 30.00", output.getvalue())
        self.assertIn("Transaction($30", output.getvalue())

if __name__ == "__main__":
    unittest.main()
