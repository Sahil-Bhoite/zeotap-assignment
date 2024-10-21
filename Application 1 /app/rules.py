from app.ast import Node  # Importing the Node class used to build the abstract syntax tree (AST)
import re  # Regular expressions for tokenizing the rule string

# Custom exception for rule engine errors
class RuleEngineError(Exception):
    pass

# Tokenizer function: Splits the input rule string into a list of tokens.
def tokenize(rule_string):
    """
    Tokenizes the rule string into a list of recognizable elements, such as parentheses, 
    operators (AND, OR, >, <, =), attributes, and values.
    
    Example:
    Input: 'age > 18 AND (income < 5000 OR credit_score >= 600)'
    Output: ['age', '>', '18', 'AND', '(', 'income', '<', '5000', 'OR', 'credit_score', '>=', '600', ')']
    
    Args:
        rule_string (str): The rule in string format.
    
    Returns:
        List[str]: A list of tokens.
    """
    tokens = re.findall(r'\(|\)|AND|OR|[<>=]+|\w+|\"[^\"]*\"|\d+', rule_string)  # Regular expression for extracting tokens
    return [token.strip('"') for token in tokens]  # Strip quotation marks from any string values

# Parsing the tokens into an AST: Parses expressions (which may contain operators like AND, OR)
def parse_expression(tokens):
    """
    Recursively parses a list of tokens into an abstract syntax tree (AST) representing the expression.
    The expression can include terms (attribute-operator-value) connected by operators like AND or OR.
    
    Args:
        tokens (List[str]): A list of tokens from the rule string.
    
    Returns:
        Node: A root node of the AST representing the entire expression.
    """
    if len(tokens) == 0:  # Base case: no tokens left to parse
        return None
    
    left = parse_term(tokens)  # Parse the first term
    
    # Parse subsequent terms connected by AND/OR operators
    while len(tokens) > 0 and tokens[0] in ['AND', 'OR']:
        operator = tokens.pop(0)  # Pop the operator (AND/OR)
        right = parse_term(tokens)  # Parse the next term
        # Combine the left and right terms with the operator into an AST node
        left = Node('operator', left=left, right=right, value=operator)
    
    return left  # Return the root node of the AST

# Parsing individual terms (attribute-operator-value expressions)
def parse_term(tokens):
    """
    Parses a single term (an attribute-operator-value triplet or a parenthesized sub-expression).
    
    Args:
        tokens (List[str]): A list of tokens from the rule string.
    
    Returns:
        Node: An AST node representing the parsed term.
    
    Raises:
        RuleEngineError: If the term is invalid (e.g., missing parts or parentheses).
    """
    if tokens[0] == '(':  # If the term starts with a parenthesis, it's a sub-expression
        tokens.pop(0)  # Remove opening parenthesis
        node = parse_expression(tokens)  # Recursively parse the sub-expression
        if tokens[0] != ')':  # Ensure there's a matching closing parenthesis
            raise RuleEngineError("Missing closing parenthesis")
        tokens.pop(0)  # Remove closing parenthesis
        return node
    
    if len(tokens) < 3:  # Ensure there are at least three tokens for a valid term (attribute, operator, value)
        raise RuleEngineError("Invalid term")
    
    # Parse the attribute, operator, and value
    attribute = tokens.pop(0)  # First token is the attribute (e.g., 'age')
    operator = tokens.pop(0)  # Second token is the operator (e.g., '>')
    value = tokens.pop(0)  # Third token is the value (e.g., '18')
    
    # Convert value to an appropriate type (int or float if possible)
    if value.isdigit():
        value = int(value)
    elif value.replace('.', '').isdigit():
        value = float(value)
    
    # Return a new AST node representing this term
    return Node('operand', value=(attribute, operator, value))

# Function to create a rule by parsing the rule string into an AST
def create_rule(rule_string):
    """
    Converts a rule string into an abstract syntax tree (AST) for further evaluation.
    
    Args:
        rule_string (str): The rule as a string.
    
    Returns:
        Node: The root node of the generated AST.
    """
    tokens = tokenize(rule_string)  # Tokenize the rule string
    return parse_expression(tokens)  # Parse the tokens into an AST

# Combines multiple ASTs into a single AST by joining them with AND operators
def combine_rules(rules):
    """
    Combines a list of ASTs into a single AST using AND operators between the rules.
    
    Args:
        rules (List[Node]): A list of root nodes (ASTs) representing individual rules.
    
    Returns:
        Node: The root node of the combined AST.
    """
    if not rules:  # If no rules are provided, return None
        return None
    combined_ast = rules[0]  # Start with the first rule
    for rule in rules[1:]:  # Combine the remaining rules using AND
        combined_ast = Node("operator", left=combined_ast, right=rule, value="AND")
    return combined_ast  # Return the combined AST

# Evaluates a node of the AST by applying its operator/operand logic to the provided data
def evaluate_node(node, data):
    """
    Recursively evaluates an AST node against the provided data.
    
    Args:
        node (Node): The AST node to evaluate.
        data (Dict): The data dictionary with values for the attributes in the rule.
    
    Returns:
        bool: The result of evaluating the node.
    
    Raises:
        RuleEngineError: If an unknown operator or attribute is encountered.
    """
    if node.node_type == "operand":  # If it's an operand node (attribute-operator-value)
        attribute, operator, value = node.value
        if attribute not in data:
            raise RuleEngineError(f"Attribute '{attribute}' not found in data")
        
        data_value = data[attribute]  # Get the value of the attribute from the data
        
        # Evaluate the operator
        if operator == ">":
            return data_value > value
        elif operator == "<":
            return data_value < value
        elif operator == "=":
            return data_value == value
        elif operator == ">=":
            return data_value >= value
        elif operator == "<=":
            return data_value <= value
        else:
            raise RuleEngineError(f"Unknown operator: {operator}")
    
    elif node.node_type == "operator":  # If it's an operator node (AND/OR)
        # Evaluate both sides of the operator
        if node.value == "AND":
            return evaluate_node(node.left, data) and evaluate_node(node.right, data)
        elif node.value == "OR":
            return evaluate_node(node.left, data) or evaluate_node(node.right, data)
    
    raise RuleEngineError(f"Unknown node type: {node.node_type}")

# Evaluates a full AST against the provided data
def evaluate_rule(ast, data):
    """
    Evaluates the entire AST against the data.
    
    Args:
        ast (Node): The root node of the AST.
        data (Dict): The data dictionary with values for the attributes in the rule.
    
    Returns:
        bool: The result of the evaluation.
    
    Raises:
        RuleEngineError: If the data format is invalid.
    """
    if not isinstance(data, dict):
        raise RuleEngineError("Invalid data format")
    return evaluate_node(ast, data)

# Serialize an AST into a dictionary format for storage
def serialize_ast(node):
    """
    Serializes an AST node into a dictionary format for storage.
    
    Args:
        node (Node): The AST node to serialize.
    
    Returns:
        Dict: The serialized node.
    """
    if node is None:
        return None
    return {
        'node_type': node.node_type,
        'value': node.value,
        'left': serialize_ast(node.left),
        'right': serialize_ast(node.right)
    }

# Deserialize a dictionary back into an AST node
def deserialize_ast(node_dict):
    """
    Deserializes a dictionary back into an AST node.
    
    Args:
        node_dict (Dict): The dictionary representing the node.
    
    Returns:
        Node: The deserialized AST node.
    """
    if node_dict is None:
        return None
    return Node(
        node_type=node_dict['node_type'],
        value=node_dict.get('value'),
        left=deserialize_ast(node_dict.get('left')),
        right=deserialize_ast(node_dict.get('right'))
    )
