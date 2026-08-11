# Personal Finance Manager — Design Patterns Project

This project is a hands-on exercise in applying Object-Oriented Design Patterns to build a simplified personal finance manager.
You will implement and extend starter code to add functionality such as tracking transactions, adapting external data, observing balance changes, and ensuring proper architectural patterns.

## Getting Started

### Dependencies

Make sure you have python version >= 3.10.x installed on your computer. 


### Installation

1. Clone the repo:

```
bash
git clone https://github.com/udacity/cd14600-project-starter.git
cd cd14600-project-starter/starter
```

2. Run the Program: 
```
python main.py
```

## Testing

This project uses Python’s built-in unittest framework.

To run all tests:

```
python -m unittest discover
```

To run a single test file:
```
python -m unittest balance/test_balance_observer.py
```

### Break Down Tests

- test_balance.py → Verifies correct implementation of the Singleton Balance class.
- test_transaction.py → Confirms transactions update balances correctly.
- test_transaction_adapter.py → Ensures external income data is correctly adapted into Transaction objects.
- test_balance_observer.py → Validates that low-balance alerts are triggered at the correct threshold.

## Project Instructions

1. Implement Singleton Balance Class – Ensure only one balance object exists throughout the app.
2. Complete Transaction Class – Handle income and expense transactions.
3. Implement Adapter Pattern – Adapt external freelance income data into internal Transaction objects.
4. Implement Observer Pattern – Create a low balance observer that triggers an alert when funds drop too low.
5. Add Unit Tests – Write tests for all implemented functionality.
6. Choose and Implement a Fourth Pattern – Pick one additional design pattern (e.g., Strategy, Command, Decorator, etc.) and integrate it into your project.
7. Provide a Reflection – Add a short write-up in your repo (README or separate file) explaining your design choices.

## Additional Pattern: Strategy

### Why Strategy was chosen

Income and expenses currently change a balance in different ways, and future
transaction types may introduce fees, interest, refunds, currency conversion,
or other calculation rules. The Strategy pattern keeps each rule in a small,
independent object instead of growing a conditional inside `Balance` whenever a
new type is introduced.

### Where it fits

`TransactionStrategy` defines the calculation interface. `IncomeStrategy` and
`ExpenseStrategy` implement the standard rules. `Balance` maps each
`TransactionCategory` to a strategy and delegates the calculation when it
applies a transaction. Additional categories can be supported through
`register_transaction_strategy()` without changing `Balance.apply_transaction()`.

### Benefits

- **Flexibility:** calculation behavior can be selected or replaced at runtime.
- **Testability:** each calculation rule can be unit tested without constructing
  the rest of the application.
- **Scalability:** new transaction rules are added as new strategy classes rather
  than additional conditional branches in the balance manager.

## Design Pattern Reflection

This application uses four design patterns: Singleton, Adapter, Observer, and
Strategy. Together, they separate balance state, external-data conversion,
notifications, and calculation rules into focused responsibilities.

### Singleton

`Balance` is a Singleton, so every caller receives the same balance manager and
there cannot be conflicting balances in different parts of the application.
This provides one consistent source of truth and avoids passing a balance object
through every layer. The trade-off is shared mutable state: tests and repeated
simulations must reset the balance, and registered observers must be managed
carefully to prevent state leaking between uses.

### Adapter

`TransactionAdapter` converts `ExternalFreelanceIncome` into the application's
standard `Transaction` representation. This keeps third-party field formats and
types out of the core balance logic. A different external provider can receive
its own adapter without changing `Balance`. The trade-off is an additional
wrapper for each incompatible external format, and the current adapter is
intentionally specialized for income transactions.

### Observer

`Balance` notifies `PrintBalanceObserver` and `LowBalanceAlertObserver` after a
transaction changes the balance. This decouples balance calculations from user
output and alert policy, making observers independently replaceable and
testable. The trade-off is lifecycle complexity: observers must be registered
and removed correctly. Notification order and errors raised by an observer also
need an explicit policy in a larger production system.

### Strategy

`IncomeStrategy` and `ExpenseStrategy` encapsulate the rules for calculating a
new balance. `Balance` selects the appropriate strategy from the transaction
category, and custom strategies can be registered without modifying its
transaction-processing method. This improves extension and unit testing as new
rules such as fees, refunds, or interest are introduced. The trade-off is more
classes and configuration than a small `if` statement, so the benefit becomes
most valuable as the number and complexity of transaction rules grows.

### Implementation challenges

The main challenge was making the patterns cooperate without mixing their
responsibilities. Because `Balance` is shared, observer registrations can also
persist and affect later tests; tests therefore remove the observers they add.
Observer notifications occur only after a strategy successfully applies a
transaction, which prevents alerts from reporting changes that never happened.
The adapter also deliberately exposes only the external amount and maps the
external record to `INCOME`, keeping provider-specific invoice details outside
the internal transaction model. These choices keep the example small and clear,
but a production application would likely add validation, persistent storage,
observer error isolation, and adapters for more external transaction types.

## Built With

* [unittest](https://docs.python.org/3/library/unittest.html) – Testing framework
* [PEP8](https://peps.python.org/pep-0008/) – Style guide for Python code
