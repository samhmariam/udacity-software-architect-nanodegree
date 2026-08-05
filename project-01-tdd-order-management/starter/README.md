# Udatracker Starter Code

This directory contains the starter code for the Udatracker project. The initial structure of directories and files is described below.

```
.
├── backend
│   ├── __init__.py
│   ├── app.py
│   ├── in_memory_storage.py
│   ├── order_tracker.py
│   ├── requirements.txt
│   └── tests
│       ├── __init__.py
│       ├── test_api.py
│       └── test_order_tracker.py
├── frontend
│   ├── css
│   │   └── style.css
│   ├── index.html
│   └── js
│       └── script.js
├── pytest.ini
└── README.md
```

## API reference

Start the application from the `starter` directory with `python -m backend.app`.
The API is then available at `http://localhost:5000`.

| Method | Endpoint | Description | Success |
| --- | --- | --- | --- |
| `POST` | `/api/orders` | Create an order | `201 Created` |
| `GET` | `/api/orders/<order_id>` | Retrieve one order | `200 OK` |
| `PUT` | `/api/orders/<order_id>/status` | Update an order's status | `200 OK` |
| `GET` | `/api/orders` | List all orders | `200 OK` |
| `GET` | `/api/orders?status=<status>` | Filter orders by status | `200 OK` |

Valid statuses are `pending`, `processing`, `shipped`, `delivered`, and
`cancelled`. Error responses contain an `error` message and use `400` for an
invalid request, `404` for an unknown order, or `409` for a duplicate order ID.

### Create an order

```bash
curl -X POST http://localhost:5000/api/orders \
  -H "Content-Type: application/json" \
  -d '{"order_id":"ORD001","item_name":"Laptop","quantity":1,"customer_id":"CUST001"}'
```

### Retrieve an order

```bash
curl http://localhost:5000/api/orders/ORD001
```

### Update an order's status

```bash
curl -X PUT http://localhost:5000/api/orders/ORD001/status \
  -H "Content-Type: application/json" \
  -d '{"new_status":"shipped"}'
```

### List or filter orders

```bash
curl http://localhost:5000/api/orders
curl "http://localhost:5000/api/orders?status=shipped"
```

## Reflection

- I kept validation and order-management rules inside `OrderTracker` while leaving the Flask routes responsible for translating requests and exceptions into HTTP responses. This separation adds a little structure, but it keeps the core behavior independent of Flask and straightforward to unit test.
- Testing invalid quantities exposed a subtle Python edge case: `bool` is a subclass of `int`, so checking only `isinstance(quantity, int)` would incorrectly accept `True`. The failing case drove an explicit boolean check in the validator.
- The API distinguishes malformed input (`400`), missing orders (`404`), and duplicate IDs (`409`). This makes failures clearer to clients, although a larger application would benefit from dedicated domain exception classes instead of inspecting exception messages.
- My next step would be replacing the in-memory store with a persistent database and repository implementation. I would also add a `DELETE` endpoint, status-transition rules, and stronger request-schema validation.
