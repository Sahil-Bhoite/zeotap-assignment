from flask import Flask

def create_app():
    """
    Creates and configures a new Flask application instance.

    Returns:
        app (Flask): A configured Flask app instance.
    """
    # Create a Flask application instance
    app = Flask(__name__)

    # Establish the application context
    with app.app_context():
        # Import and initialize the API routes from the 'api' module
        from . import api
        api.init_app(app)  # Calls the init_app function to set up routes and handlers

    # Return the configured Flask app
    return app
