from flask import Flask, request, jsonify
from datetime import datetime
import jsonschema
from jsonschema import validate

app = Flask(__name__)

# In-memory data store
event_data = {}

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

# Endpoint to receive and persist events
@app.route('/events', methods=['POST'])
def receive_events():
    try:
        data = request.get_json()

        # Validate the incoming data against the schema
        validate(data, event_schema)

        # Persist the event in the in-memory store
        event_data[data['customer_id']] = data

        return jsonify({"message": "Event received and persisted successfully"}), 200
    except jsonschema.exceptions.ValidationError as e:
        return jsonify({"error": f"Validation error: {e}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to retrieve events for a given customer ID
@app.route('/events/<customer_id>', methods=['GET'])
def get_customer_events(customer_id):
    try:
        start_time_str = request.args.get('start_time')
        end_time_str = request.args.get('end_time')

        start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M:%S') if start_time_str else None
        end_time = datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M:%S') if end_time_str else None

        # Filter events based on customer ID and optional time range
        filtered_events = [
            event for event in event_data.values() if str(event.get('customer_id')) == customer_id
            and (start_time is None or datetime.strptime(event.get('timestamp'), '%Y-%m-%dT%H:%M:%S') >= start_time)
            and (end_time is None or datetime.strptime(event.get('timestamp'), '%Y-%m-%dT%H:%M:%S') <= end_time)
        ]

        return jsonify(filtered_events), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
