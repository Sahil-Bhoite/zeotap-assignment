# Rule Engine Application

## Overview

This is a sophisticated 3-tier rule engine application that determines user eligibility based on attributes such as age, department, income, and spend. The system employs an Abstract Syntax Tree (AST) to represent conditional rules, allowing for dynamic creation, combination, and modification of these rules.

## Features

- **Create Rule**: Users can create complex rules based on given attributes.
- **Combine Rules**: Multiple rules can be combined into a single AST for more complex logic.
- **Evaluate Rule**: The system evaluates given data against the rule and returns user eligibility.
- **Error Handling**: Robust error handling for invalid rule strings and data formats, providing meaningful error messages to the user.

## Project Structure

```
.
├── app/
│   ├── api.py
│   ├── ast.py
│   ├── database.py
│   ├── rules.py
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── script.js
│   └── templates/
│       └── index.html
├── tests/
│   ├── test_rules.py
│   └── test_api.py
├── requirements.txt
├── main.py
└── README.md
```

## Design Choices

1. **3-tier Architecture**: Separates UI, API, and backend logic for improved maintainability and scalability.
2. **Abstract Syntax Tree (AST)**: Represents conditional rules, enabling dynamic creation, combination, and modification.
3. **Comprehensive Error Handling**: Ensures robustness by handling invalid rule strings and data formats.
4. **User-friendly UI**: Clean design with dynamic feedback for rule evaluation results.

## Instructions

### Prerequisites

- Python 3.6 or higher
- Flask
- SQLite (for database)

### Build and Install

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix or MacOS: `source venv/bin/activate`

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```
   python -c "from app.database import initialize_database; initialize_database()"
   ```

5. Run the application:
   ```
   python main.py
   ```

6. Open your web browser and navigate to `http://127.0.0.1:5000/`.

## Testing

### Sample UI Test

1. Create a rule:
   ```
   ((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)
   ```
   Input the above line in the "Create Rule" text box and click the "Create Rule" button. If successful, it will generate the relevant AST.

2. Evaluate a query:
   ```json
   {
     "age": 50,
     "department": "Sales",
     "salary": 60000,
     "experience": 10
   }
   ```
   Input this JSON in the "Data (JSON format):" field and click the "Evaluate" button. It will display the result as True or False.

### Running Unit Tests

To run the predefined test cases:

```
python -m unittest discover tests
```

## Contact

For more information about the developer, please visit my LinkedIn profile:
[Sahil Bhoite](https://www.linkedin.com/in/sahil-bhoite/)