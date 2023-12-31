# Event Integration Hub using Flask

This project is a simple integration hub for working with third-party systems. It provides a Flask-based API server that can receive, persist, and query structured JSON events. The events can include types such as email_open, email_click, email_unsubscribe, and purchase.

## Setup

1. Install Flask:

    ```bash
    pip install Flask jsonschema
    ```

2. Run the Flask server:

    ```bash
    python app.py
    ```

## API Endpoints

### 1. Receive and Persist Events

Use the `/events` endpoint to send events to the integration hub.

Example:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"customer_id": 123, "event_type": "email_click", "timestamp": "2023-10-23T14:30:00", "email_id": 1234, "clicked_link": "https://example.com/some-link"}' http://127.0.0.1:5000/events

curl -X POST -H "Content-Type: application/json" -d '{"customer_id":  456, "event_type":  "email_open", "timestamp":  "2023-10-24T11:30:00", "email_id":  998}' http://127.0.0.1:5000/events

curl -X POST -H "Content-Type: application/json" -d '{"customer_id":  456, "event_type":  "email_unsubscribe", "timestamp":  "2023-10-24T11:30:25", "email_id":  998}' http://127.0.0.1:5000/events

curl -X POST -H "Content-Type: application/json" -d '{"customer_id":  123, "event_type":  "purchase", "timestamp":  "25-10-2023T15:33:00", "email_id":1234, "product_id": 357, "amount":  49.99}
' http://127.0.0.1:5000/events





```
###  2. Retrieve Events for a Customer ID

Use the /events/<customer_id> endpoint to retrieve events for a specific customer ID.

Example:
```bash
curl http://127.0.0.1:5000/events/123

curl http://127.0.0.1:5000/events/123?start_time=2023-10-23T00:00:00&end_time=2023-10-24T23:59:59

```
###  3. Testing
```bash
python -m unittest test_app.py
