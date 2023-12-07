import json
import unittest
from app import app

class TestEventIntegrationHub(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

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

    def test_get_customer_events(self):
        event_data = {
            "customer_id": 456,
            "event_type": "email_open",
            "timestamp": "2023-10-24T11:30:00",
            "email_id": 998
        }

        self.app.post('/events', json=event_data)

        response = self.app.get('/events/456')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.get_data(as_text=True))[0], event_data)

    def test_get_customer_events_with_time_range(self):
        event_data = {
            "customer_id": 123,
            "event_type": "email_click",
            "timestamp": "2023-10-23T14:30:00",
            "email_id": 1234,
            "clicked_link": "https://example.com/some-link"
        }

        self.app.post('/events', json=event_data)

        response = self.app.get('/events/123?start_time=2023-10-23T00:00:00&end_time=2023-10-24T23:59:59')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.get_data(as_text=True))[0], event_data)

if __name__ == '__main__':
    unittest.main()
