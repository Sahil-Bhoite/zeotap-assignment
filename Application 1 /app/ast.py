class Node:
    """
    This class represents a node in an abstract syntax tree (AST). Each node can either be an operator (e.g., AND, OR) 
    or an operand (e.g., a comparison like "age > 18").
    
    Attributes:
        node_type (str): The type of node ('operator' or 'operand').
        left (Node, optional): The left child node (for operators).
        right (Node, optional): The right child node (for operators).
        value (any): The value of the node. For an operand, it's a tuple containing the attribute, operator, and value. 
                     For an operator, it's the type of operation (e.g., 'AND' or 'OR').
    """
    
    def __init__(self, node_type, left=None, right=None, value=None):
        """
        Initializes a Node with the specified type and optional children and value.
        
        Args:
            node_type (str): Type of the node, either 'operator' (e.g., AND, OR) or 'operand' (e.g., a condition).
            left (Node, optional): The left child node (for operators).
            right (Node, optional): The right child node (for operators).
            value (any): The value of the node. For operands, this could be a condition like ("age", ">", 18). 
                         For operators, it could be "AND" or "OR".
        """
        self.node_type = node_type  # Type of the node ('operator' or 'operand')
        self.left = left  # Left child node (for operators)
        self.right = right  # Right child node (for operators)
        self.value = value  # Value of the node (either the condition for operands, or the operator type for operators)
    
    def __repr__(self):
        """
        Returns a string representation of the node for debugging purposes.
        
        Returns:
            str: A string that represents the node, including its type, value, and its left and right children.
        """
        return f"Node({self.node_type}, {self.value}, {self.left}, {self.right})"
