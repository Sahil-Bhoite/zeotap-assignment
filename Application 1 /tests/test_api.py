import unittest
import json
from app import create_app
from app.rules import RuleEngineError

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

    def test_create_rule_api_success(self):
        rule_string = "age > 30 AND department = 'Sales'"
        response = self.client.post('/create_rule', data=json.dumps({'rule_string': rule_string}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        self.assertIn('message', response.json)

    def test_create_rule_api_failure(self):
        rule_string = "invalid rule"
        response = self.client.post('/create_rule', data=json.dumps({'rule_string': rule_string}), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['status'], 'error')
        self.assertIn('message', response.json)

    def test_evaluate_rule_api_success(self):
        rule_string = "age > 30 AND department = 'Sales'"
        data = {"age": 35, "department": "Sales"}
        response = self.client.post('/evaluate_rule', data=json.dumps({'rule_string': rule_string, 'data': data}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        self.assertTrue(response.json['result'])

    def test_evaluate_rule_api_failure(self):
        rule_string = "age > 30 AND department = 'Sales'"
        data = {"age": 25, "department": "Marketing"}
        response = self.client.post('/evaluate_rule', data=json.dumps({'rule_string': rule_string, 'data': data}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        self.assertFalse(response.json['result'])

    def test_evaluate_rule_api_invalid_data(self):
        rule_string = "age > 30 AND department = 'Sales'"
        data = {"age": "invalid", "department": "Sales"}
        response = self.client.post('/evaluate_rule', data=json.dumps({'rule_string': rule_string, 'data': data}), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['status'], 'error')
        self.assertIn('message', response.json)

    def test_not_found(self):
        response = self.client.get('/non_existent_route')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['status'], 'error')
        self.assertIn('message', response.json)

if __name__ == '__main__':
    unittest.main()