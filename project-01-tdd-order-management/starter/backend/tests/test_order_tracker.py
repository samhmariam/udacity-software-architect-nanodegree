from unittest.mock import Mock

import pytest

from ..order_tracker import OrderTracker

# --- Fixtures for Unit Tests ---


@pytest.fixture
def mock_storage():
    """
    Provides a mock storage object for tests.
    This mock will be configured to simulate various storage behaviors.
    """
    mock = Mock()
    # By default, mock get_order to return None (no order found)
    mock.get_order.return_value = None
    # By default, mock get_all_orders to return an empty dict
    mock.get_all_orders.return_value = {}
    return mock


@pytest.fixture
def order_tracker(mock_storage):
    """
    Provides an OrderTracker instance initialized with the mock_storage.
    """
    return OrderTracker(mock_storage)


def test_add_order_successfully(order_tracker, mock_storage):
    """Tests adding a new order with default 'pending' status."""
    result = order_tracker.add_order("ORD001", "Laptop", 1, "CUST001")

    expected_order = {
        "order_id": "ORD001",
        "item_name": "Laptop",
        "quantity": 1,
        "customer_id": "CUST001",
        "status": "pending",
    }
    assert result == expected_order
    mock_storage.save_order.assert_called_once_with("ORD001", expected_order)


def test_add_order_raises_error_if_exists(order_tracker, mock_storage):
    """Tests that adding an order with a duplicate ID raises a ValueError."""
    # Simulate that the storage finds an existing order
    mock_storage.get_order.return_value = {"order_id": "ORD_EXISTING"}

    error_message = "Order with ID 'ORD_EXISTING' already exists."
    with pytest.raises(ValueError, match=error_message):
        order_tracker.add_order("ORD_EXISTING", "New Item", 1, "CUST001")


@pytest.mark.parametrize("field_index", range(3))
def test_add_order_rejects_empty_string_fields(order_tracker, field_index):
    values = ["ORD001", "Laptop", "CUST001"]
    values[field_index] = "  "

    with pytest.raises(ValueError, match="non-empty string"):
        order_tracker.add_order(values[0], values[1], 1, values[2])


@pytest.mark.parametrize("quantity", [0, -1, 1.5, "1", True])
def test_add_order_rejects_invalid_quantity(order_tracker, quantity):
    with pytest.raises(ValueError, match="positive integer"):
        order_tracker.add_order("ORD001", "Laptop", quantity, "CUST001")


def test_add_order_rejects_invalid_status(order_tracker):
    with pytest.raises(ValueError, match="must be one of"):
        order_tracker.add_order("ORD001", "Laptop", 1, "CUST001", "unknown")


def test_get_order_by_id_returns_existing_order(order_tracker, mock_storage):
    expected_order = {
        "order_id": "ORD001",
        "item_name": "Laptop",
        "quantity": 1,
        "customer_id": "CUST001",
        "status": "pending",
    }
    mock_storage.get_order.return_value = expected_order

    result = order_tracker.get_order_by_id("ORD001")

    assert result == expected_order
    mock_storage.get_order.assert_called_once_with("ORD001")


def test_get_order_by_id_returns_none_if_order_missing(order_tracker, mock_storage):
    assert order_tracker.get_order_by_id("MISSING") is None
    mock_storage.get_order.assert_called_once_with("MISSING")


def test_get_order_by_id_rejects_empty_id(order_tracker, mock_storage):
    with pytest.raises(ValueError, match="non-empty string"):
        order_tracker.get_order_by_id("  ")

    mock_storage.get_order.assert_not_called()


def test_update_order_status_saves_and_returns_updated_order(
    order_tracker, mock_storage
):
    mock_storage.get_order.return_value = {
        "order_id": "ORD001",
        "item_name": "Laptop",
        "quantity": 1,
        "customer_id": "CUST001",
        "status": "pending",
    }

    result = order_tracker.update_order_status("ORD001", "delivered")

    assert result["status"] == "delivered"
    mock_storage.save_order.assert_called_once_with("ORD001", result)


def test_update_order_status_raises_error_if_order_missing(order_tracker):
    with pytest.raises(LookupError, match="was not found"):
        order_tracker.update_order_status("MISSING", "shipped")


def test_update_order_status_rejects_invalid_status(order_tracker, mock_storage):
    with pytest.raises(ValueError, match="must be one of"):
        order_tracker.update_order_status("ORD001", "in-transit")

    mock_storage.get_order.assert_not_called()
    mock_storage.save_order.assert_not_called()


def test_list_all_orders_returns_every_order(order_tracker, mock_storage):
    orders = {
        "ORD001": {"order_id": "ORD001", "status": "pending"},
        "ORD002": {"order_id": "ORD002", "status": "shipped"},
    }
    mock_storage.get_all_orders.return_value = orders

    result = order_tracker.list_all_orders()

    assert result == list(orders.values())
    mock_storage.get_all_orders.assert_called_once_with()


def test_list_orders_by_status_returns_only_matching_orders(
    order_tracker, mock_storage
):
    pending_order = {"order_id": "ORD001", "status": "pending"}
    shipped_order = {"order_id": "ORD002", "status": "shipped"}
    mock_storage.get_all_orders.return_value = {
        "ORD001": pending_order,
        "ORD002": shipped_order,
        "ORD003": {"order_id": "ORD003", "status": "processing"},
    }

    result = order_tracker.list_orders_by_status("shipped")

    assert result == [shipped_order]
    mock_storage.get_all_orders.assert_called_once_with()


def test_list_orders_by_status_returns_empty_list_when_none_match(
    order_tracker, mock_storage
):
    mock_storage.get_all_orders.return_value = {
        "ORD001": {"order_id": "ORD001", "status": "pending"},
    }

    result = order_tracker.list_orders_by_status("shipped")

    assert result == []
    mock_storage.get_all_orders.assert_called_once_with()
