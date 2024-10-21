from sqlalchemy import create_engine, Column, Integer, String, LargeBinary  # Import SQLAlchemy components
from sqlalchemy.ext.declarative import declarative_base  # Base class for ORM models
from sqlalchemy.orm import sessionmaker  # Session maker for handling database transactions
import json  # For serializing and deserializing the AST

# Define the base class for ORM models
Base = declarative_base()

# Define the Rule model representing the "rules" table in the database
class Rule(Base):
    """
    This class represents the 'rules' table in the database.
    It stores the rule string and its corresponding abstract syntax tree (AST) in binary form.
    
    Columns:
        id: Primary key, auto-incrementing integer.
        rule_string: The rule in string format.
        ast: The abstract syntax tree (AST) serialized and stored as a binary blob.
    """
    __tablename__ = 'rules'  # Name of the table
    id = Column(Integer, primary_key=True)  # Primary key, unique identifier for each rule
    rule_string = Column(String, nullable=False)  # The rule string itself (e.g., "age > 18 AND income < 5000")
    ast = Column(LargeBinary, nullable=False)  # The AST in serialized binary form

# Create a SQLite database engine. The database will be stored in a file named "rule_engine.db"
engine = create_engine('sqlite:///rule_engine.db')

# Create a session maker bound to the engine, which will be used to interact with the database
Session = sessionmaker(bind=engine)

# Function to initialize the database schema (create tables)
def initialize_database():
    """
    Initializes the database by creating all tables defined in the ORM models (if they don't exist already).
    """
    Base.metadata.create_all(engine)  # Create all tables defined in the Base class (including the 'rules' table)

# Function to save a new rule into the database
def save_rule(rule_string, ast):
    """
    Saves a rule into the database.
    
    Args:
        rule_string (str): The rule in string format.
        ast (dict): The abstract syntax tree (AST) in dictionary format.
    
    The AST is serialized to JSON and then encoded as binary before saving to the database.
    """
    session = Session()  # Start a new session to interact with the database
    try:
        # Create a new Rule object with the rule string and the serialized AST
        new_rule = Rule(rule_string=rule_string, ast=json.dumps(ast).encode())  # Encode AST as binary
        session.add(new_rule)  # Add the new rule to the session
        session.commit()  # Commit the session to save changes to the database
    except Exception as e:
        session.rollback()  # Rollback changes if there is an error
        raise e  # Re-raise the exception for higher-level handling
    finally:
        session.close()  # Ensure the session is closed

# Function to load all rules from the database
def load_rules():
    """
    Loads all rules from the database.
    
    Returns:
        List[Tuple[str, dict]]: A list of tuples, where each tuple contains the rule string and its corresponding AST (deserialized).
    """
    session = Session()  # Start a new session to interact with the database
    try:
        # Query all rules from the 'rules' table
        rules = session.query(Rule).all()
        # Deserialize the binary AST back into its original dictionary format
        return [(rule.rule_string, json.loads(rule.ast.decode())) for rule in rules]  # Return rule string and decoded AST
    except Exception as e:
        raise e  # Re-raise the exception for higher-level handling
    finally:
        session.close()  # Ensure the session is closed

# Initialize the database (create tables if they don't exist)
initialize_database()
