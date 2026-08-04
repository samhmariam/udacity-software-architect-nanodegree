# This module contains the OrderTracker class, which encapsulates the core
# business logic for managing orders.


class OrderTracker:
    """
    Manages customer orders, providing functionalities to add, update,
    and retrieve order information.
    """
    VALID_STATUSES = frozenset({
        "pending",
        "processing",
        "shipped",
        "delivered",
        "cancelled",
    })

    def __init__(self, storage):
        required_methods = ['save_order', 'get_order', 'get_all_orders']
        for method in required_methods:
            if not hasattr(storage, method) or not callable(getattr(storage, method)):
                raise TypeError(
                    f"Storage object must implement a callable '{method}' method."
                )
        self.storage = storage

    def add_order(
        self,
        order_id: str,
        item_name: str,
        quantity: int,
        customer_id: str,
        status: str = "pending",
    ):
        self._validate_non_empty_string(order_id, "order_id")
        self._validate_non_empty_string(item_name, "item_name")
        self._validate_quantity(quantity)
        self._validate_non_empty_string(customer_id, "customer_id")
        self._validate_status(status)

        if self.storage.get_order(order_id) is not None:
            raise ValueError(f"Order with ID '{order_id}' already exists.")

        order = {
            "order_id": order_id,
            "item_name": item_name,
            "quantity": quantity,
            "customer_id": customer_id,
            "status": status,
        }
        self.storage.save_order(order_id, order)
        return order.copy()

    def get_order_by_id(self, order_id: str):
        self._validate_non_empty_string(order_id, "order_id")
        return self.storage.get_order(order_id)

    def update_order_status(self, order_id: str, new_status: str):
        self._validate_non_empty_string(order_id, "order_id")
        self._validate_status(new_status)

        order = self.storage.get_order(order_id)
        if order is None:
            raise LookupError(f"Order with ID '{order_id}' was not found.")

        order["status"] = new_status
        self.storage.save_order(order_id, order)
        return order.copy()

    def list_all_orders(self):
        return list(self.storage.get_all_orders().values())

    def list_orders_by_status(self, status: str):
        self._validate_status(status)
        return [
            order
            for order in self.storage.get_all_orders().values()
            if order.get("status") == status
        ]

    @staticmethod
    def _validate_non_empty_string(value, field_name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"'{field_name}' must be a non-empty string.")

    @staticmethod
    def _validate_quantity(quantity):
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("'quantity' must be a positive integer.")

    @classmethod
    def _validate_status(cls, status):
        if not isinstance(status, str) or status not in cls.VALID_STATUSES:
            allowed = ", ".join(sorted(cls.VALID_STATUSES))
            raise ValueError(f"'status' must be one of: {allowed}.")
