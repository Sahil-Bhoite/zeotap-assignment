import unittest
from app.rules import create_rule, evaluate_rule, RuleEngineError

class TestRules(unittest.TestCase):
    def test_create_rule_simple(self):
        rule_string = "age > 30"
        ast = create_rule(rule_string)
        self.assertIsNotNone(ast)
        self.assertEqual(ast.node_type, 'operand')
        self.assertEqual(ast.value, ('age', '>', 30))

    def test_create_rule_complex(self):
        rule_string = "(age > 30 AND department = 'Sales') OR (experience > 5)"
        ast = create_rule(rule_string)
        self.assertIsNotNone(ast)
        self.assertEqual(ast.node_type, 'operator')
        self.assertEqual(ast.value, 'OR')

    def test_create_rule_invalid(self):
        rule_string = "invalid rule"
        with self.assertRaises(RuleEngineError):
            create_rule(rule_string)

    def test_evaluate_rule_true(self):
        rule_string = "age > 30 AND department = 'Sales'"
        ast = create_rule(rule_string)
        data = {"age": 35, "department": "Sales"}
        result = evaluate_rule(ast, data)
        self.assertTrue(result)

    def test_evaluate_rule_false(self):
        rule_string = "age > 30 AND department = 'Sales'"
        ast = create_rule(rule_string)
        data = {"age": 25, "department": "Sales"}
        result = evaluate_rule(ast, data)
        self.assertFalse(result)

    def test_evaluate_rule_missing_data(self):
        rule_string = "age > 30 AND department = 'Sales'"
        ast = create_rule(rule_string)
        data = {"age": 35}
        with self.assertRaises(RuleEngineError):
            evaluate_rule(ast, data)

    def test_evaluate_rule_invalid_data_type(self):
        rule_string = "age > 30"
        ast = create_rule(rule_string)
        data = {"age": "thirty"}
        with self.assertRaises(RuleEngineError):
            evaluate_rule(ast, data)

    def test_complex_rule_evaluation(self):
        rule_string = "(age > 30 OR experience > 5) AND (department = 'Sales' OR department = 'Marketing')"
        ast = create_rule(rule_string)
        data1 = {"age": 35, "experience": 3, "department": "Sales"}
        data2 = {"age": 28, "experience": 7, "department": "Marketing"}
        data3 = {"age": 25, "experience": 2, "department": "IT"}
        self.assertTrue(evaluate_rule(ast, data1))
        self.assertTrue(evaluate_rule(ast, data2))
        self.assertFalse(evaluate_rule(ast, data3))

if __name__ == '__main__':
    unittest.main()