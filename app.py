"""
app.py

This module sets up and runs the Flask application, handling errors and
integrating ASGI support for better performance and scalability.

It imports necessary modules and registers the blueprint for application views.
"""

from flask_server import app
from asgiref.wsgi import WsgiToAsgi
from flask_server.views.v1 import app_views

@app.errorhandler(404)
def page_not_found(error):
    """
    Handle 404 Page Not Found errors.

    Args:
        error: The error object representing the 404 error.

    Returns:
        tuple: A tuple containing an error message and the HTTP status code 404.
    """
    return 'This page does not exist', 404

if __name__ == '__main__':
    # Register the blueprint for application views
    app.register_blueprint(app_views)

    # Wrap the Flask app with the ASGI middleware for ASGI compatibility
    app = WsgiToAsgi(app)

    # Run the Flask app using Uvicorn
    import uvicorn
    uvicorn.run(app, host="127.0.0.2", port=5000)
