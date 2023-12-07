# Define JSON schema for events

event_schema = {
    "type": "object",
    "properties": {
        "customer_id": {"type": "integer"},
        "event_type": {"type": "string"},
        "timestamp": {"type": "string", "format": "date-time"},
        "email_id": {"type": "integer"},
        "clicked_link": {"type": "string", "format": "uri"},
        "product_id": {"type": "integer"},
        "amount": {"type": "number"},
    },
    "required": ["customer_id", "event_type", "timestamp"],
}