# Order Management Service

Build a minimal order-tracking application using test-driven development (TDD). The project combines a framework-independent domain layer, a Flask REST API, in-memory storage, and a small frontend.

## Project scenario

You are a software engineer at a small e-commerce startup. Your goal is to develop an order-tracking service by writing tests before implementation code.

Begin with failing tests that describe the expected behavior of an `OrderTracker` class. Implement only enough code to pass those tests, improve the design while keeping the suite green, and then repeat the cycle:

1. **Red:** Write a test that fails for the expected reason.
2. **Green:** Add the smallest implementation that makes it pass.
3. **Refactor:** Improve the code without changing its behavior.

Once the domain logic is well tested, expose it through a Flask API and connect the frontend.

## Functional requirements

The completed application must allow a user to:

- create an order;
- retrieve an order by ID;
- update an order's status, such as from `pending` to `shipped`;
- list all orders;
- filter orders by status.

The service must reject duplicate order IDs and invalid updates. Orders are stored in memory, so all data is cleared whenever the application restarts.

> **Note:** This project implements create, read, and update operations. Deleting orders is outside its current scope.

## Architecture

Keep business rules separate from HTTP concerns:

- **Domain layer:** The `OrderTracker` owns order-management rules, including duplicate prevention, validation, lookup, updates, and filtering.
- **API layer:** Flask routes translate HTTP requests into calls to the domain layer and return appropriate responses.
- **Presentation layer:** A lightweight frontend consumes the REST API.
- **Storage:** An in-memory data store keeps the project simple and deterministic.

This separation makes the core behavior easy to test without starting a web server and keeps the Flask integration thin.

## Testing approach

Use `pytest` to test the application at two levels:

### Unit tests

Test `OrderTracker` behavior in isolation, including:

- successful order creation;
- rejection of duplicate IDs;
- retrieval of existing and missing orders;
- valid and invalid status updates;
- listing and status-based filtering.

### API tests

Use Flask's test client to verify:

- request parsing and validation;
- response bodies and HTTP status codes;
- integration between routes and the domain layer;
- error responses for invalid or missing data.

Keep each test focused on one behavior, use descriptive names, and run the full suite after every refactor.

## Learning outcomes

By completing this project, you will be able to:

- apply the Red–Green–Refactor cycle;
- use tests to guide business-logic design;
- write maintainable unit and API tests with `pytest`;
- build and test a RESTful Flask API;
- separate domain logic from framework code;
- diagnose defects through focused test failures;
- explain how disciplined TDD improves real-world systems.

## Completion checklist

- [ ] Core behavior was developed test-first.
- [ ] All functional requirements are covered by tests.
- [ ] Domain logic does not depend on Flask.
- [ ] API routes return consistent responses and status codes.
- [ ] Duplicate IDs and invalid updates are handled explicitly.
- [ ] The frontend can create, view, update, list, and filter orders.
- [ ] The complete test suite passes.
- [ ] A short reflection describes what you learned from applying TDD.

## Reflection prompts

After running the completed application, briefly consider:

- How did writing tests first affect your implementation choices?
- Which failure was most useful while debugging?
- Where did refactoring improve the design?
- What would need to change before using this service in production?
