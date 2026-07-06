import unittest
import os
import sys

# Ensure the script runs in the directory of the file so it loads the pkl files correctly
sys.path.append(os.path.dirname(__file__))

from app import app

class CreditAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def get_valid_data(self):
        return {
            'full-name': 'John Doe',
            'gender': 'M',
            'car': 'Y',
            'realty': 'Y',
            'children': '0',
            'income': '50000',
            'income-type': 'Working',
            'education': 'Higher education',
            'family-status': 'Married',
            'housing-type': 'House / apartment',
            'age': '30',
            'work-exp': '5',
            'family-size': '2',
            'phone': '1234567890',
            'email': 'test@example.com',
            'occupation': 'Laborers'
        }

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Credit Card Prediction', response.data)

    def test_about_page(self):
        response = self.app.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Credit Card Prediction', response.data)

    def test_404_handler(self):
        response = self.app.get('/nonexistent-page')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'404 - Page Not Found', response.data)

    def test_inquiries_page(self):
        response = self.app.get('/inquiries')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Application Inquiries', response.data)

    def test_reports_page(self):
        response = self.app.get('/reports')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Operational Analytics', response.data)

    def test_predict_endpoint_valid(self):
        data = self.get_valid_data()
        response = self.app.post('/predict', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Application Approved' in response.data or b'Application Declined' in response.data)

    def test_predict_endpoint_invalid_type(self):
        data = self.get_valid_data()
        data['income'] = 'invalid_income_value'
        response = self.app.post('/predict', data=data)
        self.assertEqual(response.status_code, 400)
        json_data = response.get_json()
        self.assertEqual(json_data['error'], 'validation_error')
        self.assertEqual(json_data['details'][0]['field'], 'income')

    def test_predict_endpoint_unseen_category(self):
        data = self.get_valid_data()
        data['income-type'] = 'SuperWorking'
        response = self.app.post('/predict', data=data)
        self.assertEqual(response.status_code, 400)
        json_data = response.get_json()
        self.assertEqual(json_data['error'], 'validation_error')
        self.assertEqual(json_data['field'], 'NAME_INCOME_TYPE')
        self.assertIn('Unrecognized category value', json_data['message'])

if __name__ == '__main__':
    unittest.main()
