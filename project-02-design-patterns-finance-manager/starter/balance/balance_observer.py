# balance_observer.py

class IBalanceObserver:
    def update(self, balance, transaction):
        """Handle balance updates."""
        raise NotImplementedError("Subclasses must implement update method.")


class PrintBalanceObserver(IBalanceObserver):
    def update(self, balance, transaction):
        """Print balance update message."""
        print(f"Balance updated: {balance.summary()} after {transaction}")


class PrintObserver(PrintBalanceObserver):
    """Backward-compatible name for the print balance observer."""


class LowBalanceAlertObserver(IBalanceObserver):
    def __init__(self, threshold):
        self.threshold = threshold
        self.alert_triggered = False

    def update(self, balance, transaction):
        """Alert if balance drops below threshold."""
        self.alert_triggered = balance.get_balance() < self.threshold
        if self.alert_triggered:
            print(
                "Low balance alert: "
                f"{balance.get_balance():.2f} is below {self.threshold:.2f}"
            )
