import json
import unittest
from app import app
from data import db
import sqlite3

class TestEventIntegrationHub(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        db.create_table()  # Ensure the table exists in the SQLite database

    def tearDown(self):
        # Optional: Clean up the database after each test
        connection = sqlite3.connect("event_database.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM events")
        connection.commit()
        cursor.close()

    def test_receive_and_persist_event(self):
        event_data = {
            "customer_id": 123,
            "event_type": "email_click",
            "timestamp": "2023-10-23T14:30:00",
            "email_id": 1234,
            "clicked_link": "https://example.com/some-link"
        }

        response = self.app.post('/events', json=event_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.get_data(as_text=True)), {"message": "Event received and persisted successfully"})

        # Verify the event is in the database
        connection = sqlite3.connect("event_database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM events WHERE customer_id = 123")
        result = cursor.fetchone()
        cursor.close()

        self.assertIsNotNone(result)
        self.assertEqual(result[1], 123)  # Assuming the second column is 'customer_id'

    def test_get_customer_events(self):
        # Add an event to the database
        self.app.post('/events', json={
            "customer_id": 456,
            "event_type": "email_open",
            "timestamp": "2023-10-24T11:30:00",
            "email_id": 998
        })

        response = self.app.get('/events/456')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.get_data(as_text=True))[0]['customer_id'], 456)

    def test_get_customer_events_with_time_range(self):
        # Add an event to the database
        self.app.post('/events', json={
            "customer_id": 123,
            "event_type": "email_click",
            "timestamp": "2023-10-23T14:30:00",
            "email_id": 1234,
            "clicked_link": "https://example.com/some-link"
        })

        response = self.app.get('/events/123?start_time=2023-10-23T00:00:00&end_time=2023-10-24T23:59:59')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.get_data(as_text=True))[0]['customer_id'], 123)

if __name__ == '__main__':
    unittest.main()
