# Nirikshak.AI — API Reference

Base URL: `http://localhost:8000/api`

---

## 1. Customers

### `GET /customers/`
List all customers.
* **Query Params:** `skip` (int), `limit` (int)
* **Response:** Array of Customer objects.

### `GET /customers/{customer_id}`
Get a full Customer 360 view, including aggregated financial data and active triggers.
* **Response:**
  ```json
  {
    "id": 1,
    "name": "Rahul Singh",
    "financial_health_score": 85.5,
    "total_credits": 150000.0,
    "total_debits": 95000.0,
    "top_spend_categories": [...],
    "product_holdings": ["Savings Account", "Health Insurance"],
    "active_triggers": 2
  }
  ```

---

## 2. Transactions

### `GET /transactions/`
List transactions.
* **Query Params:** `customer_id` (int), `category` (str)
* **Response:** Array of Transaction objects.

---

## 3. Triggers (Nudges)

### `GET /triggers/`
List generated triggers.
* **Query Params:** `customer_id` (int), `status` (str: pending, accepted, dismissed)
* **Response:** Array of Trigger objects.

### `POST /triggers/scan`
**Core Action:** Runs the Pattern Detection Engine and RAG pipeline for a customer.
* **Request Body:**
  ```json
  {
    "customer_id": 1
  }
  ```
* **Response:**
  ```json
  {
    "customer_id": 1,
    "triggers_found": 2,
    "triggers": [...] // List of newly created triggers
  }
  ```

---

## 4. Feedback

### `POST /feedback/`
Submit customer feedback (accept/dismiss) on a trigger.
* **Request Body:**
  ```json
  {
    "trigger_id": 42,
    "customer_id": 1,
    "action": "accepted"
  }
  ```
* **Response:** The created feedback object.

---

## 5. Analytics (Admin)

### `GET /analytics/overview`
Get aggregate system performance data for the admin dashboard.
* **Response:**
  ```json
  {
    "total_customers": 20,
    "total_triggers": 45,
    "total_accepted": 12,
    "acceptance_rate": 26.6,
    "trigger_type_breakdown": [...],
    "conversion_trend": [...]
  }
  ```
