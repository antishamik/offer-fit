from flask import Flask, request, jsonify
from datetime import datetime
import jsonschema
from jsonschema import validate
import sqlite3
from sqlite3 import Error

from data import db
from data import schema

app = Flask(__name__)


# Initialize the SQLite table
db.create_table()


# Endpoint to receive and persist events
@app.route('/events', methods=['POST'])
def receive_events():
    try:
        data = request.get_json()

        # Validate the incoming data against the schema
        validate(data, schema.event_schema)

        # Persist the event in the SQLite database
        connection = sqlite3.connect(db.db_file)
        cursor = connection.cursor()

        cursor.execute('''
            INSERT INTO events (customer_id, event_type, timestamp, email_id, clicked_link, product_id, amount)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['customer_id'], data['event_type'], data['timestamp'],
            data.get('email_id'), data.get('clicked_link'), data.get('product_id'), data.get('amount')
        ))

        connection.commit()
        cursor.close()

        return jsonify({"message": "Event received and persisted successfully"}), 200
    except jsonschema.exceptions.ValidationError as e:
        return jsonify({"error": f"Validation error: {e}"}), 400
    except Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500
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

        # Retrieve events from the SQLite database
        connection = sqlite3.connect(db.db_file)
        cursor = connection.cursor()

        cursor.execute('''
            SELECT * FROM events
            WHERE customer_id = ? AND
                  ( ? IS NULL OR timestamp >= ?) AND
                  ( ? IS NULL OR timestamp <= ?)
        ''', (customer_id, start_time, start_time, end_time, end_time))

        rows = cursor.fetchall()
        cursor.close()

        # Convert SQLite rows to a list of dictionaries
        events = [dict(zip(['event_id', 'customer_id', 'event_type', 'timestamp', 'email_id', 'clicked_link', 'product_id', 'amount'], row)) for row in rows]

        return jsonify(events), 200
    except Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
