from flask import request, jsonify, render_template
from app.rules import create_rule, evaluate_rule, RuleEngineError
from marshmallow import Schema, fields, ValidationError

# Schema definition for creating a rule using Marshmallow
class RuleSchema(Schema):
    rule_string = fields.Str(required=True)  # Defines that the 'rule_string' field is required and must be a string

# Schema definition for evaluating a rule using Marshmallow
class EvaluationSchema(Schema):
    rule_string = fields.Str(required=True)  # 'rule_string' is required to define the rule to evaluate
    data = fields.Dict(required=True)  # 'data' is required to pass in the data to be evaluated against the rule

def init_app(app):
    """
    Initializes the Flask app with routes for rule creation, evaluation, and error handling.
    
    Args:
        app: The Flask application instance.
    """

    @app.route('/')
    def index():
        """
        Route to serve the home page. It renders an HTML template 'index.html'.
        
        Returns:
            A rendered HTML page.
        """
        return render_template('index.html')

    @app.route('/create_rule', methods=['POST'])
    def create_rule_api():
        """
        API endpoint to create a rule from a rule string.
        
        Receives a JSON payload with a rule string, validates the input, creates the abstract syntax tree (AST) for the rule,
        and returns a success message or an error message if something goes wrong.
        
        Returns:
            JSON response with success or error messages.
        """
        schema = RuleSchema()  # Initialize the RuleSchema for input validation
        try:
            # Validate and load the request data using the schema
            data = schema.load(request.json)
        except ValidationError as err:
            # Return validation error messages if input validation fails
            return jsonify({"status": "error", "message": err.messages}), 400

        try:
            # Create the abstract syntax tree (AST) from the rule string
            ast = create_rule(data['rule_string'])
            return jsonify({"status": "success", "message": "Rule created successfully"})
        except RuleEngineError as e:
            # Return error message if rule creation fails
            return jsonify({"status": "error", "message": str(e)}), 400

    @app.route('/evaluate_rule', methods=['POST'])
    def evaluate_rule_api():
        """
        API endpoint to evaluate a rule using a provided rule string and data.
        
        Receives a JSON payload with a rule string and a data dictionary. The rule is evaluated against the data and the result 
        is returned, or an error message if evaluation fails.
        
        Returns:
            JSON response with the evaluation result or an error message.
        """
        schema = EvaluationSchema()  # Initialize the EvaluationSchema for input validation
        try:
            # Validate and load the request data using the schema
            data = schema.load(request.json)
        except ValidationError as err:
            # Return validation error messages if input validation fails
            return jsonify({"status": "error", "message": err.messages}), 400

        try:
            # Create the abstract syntax tree (AST) from the rule string
            ast = create_rule(data['rule_string'])
            # Evaluate the rule's AST against the provided data
            result = evaluate_rule(ast, data['data'])
            return jsonify({"status": "success", "result": result})
        except RuleEngineError as e:
            # Return error message if rule evaluation fails
            return jsonify({"status": "error", "message": str(e)}), 400

    @app.errorhandler(404)
    def not_found(error):
        """
        Custom error handler for 404 Not Found errors.
        
        Returns:
            JSON response with an error message indicating that the route was not found.
        """
        return jsonify({"status": "error", "message": "Not found"}), 404

    @app.errorhandler(500)
    def server_error(error):
        """
        Custom error handler for 500 Internal Server Error.
        
        Returns:
            JSON response with an error message indicating that an internal server error occurred.
        """
        return jsonify({"status": "error", "message": "Internal server error"}), 500
