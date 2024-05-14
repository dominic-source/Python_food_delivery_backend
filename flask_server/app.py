from flask_server import app
from asgiref.wsgi import WsgiToAsgi

# Import the app views
from flask_server.views.v1 import app_views

# from flask_server.auth import Auth
# # Initialize authentication setup for view functions
# auth = Auth()

@app.errorhandler(404)
def page_not_found():
    """Handle page not found"""
    return 'This page does not exist', 404


if __name__ == '__main__':
    app.register_blueprint(app_views)

    # Wrap the Flask app with the ASGIProxyMiddleware
    app = WsgiToAsgi(app)

    # Run the Flask app
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
