from flask_server import app
from flask_server.views.v1 import app_views
from asgiref.wsgi import WsgiToAsgi


@app.errorhandler(404)
def page_not_found():
    """Handle page not found"""
    return 'This page does not exist', 404


if __name__ == '__main__':
    # Wrap the Flask app with the ASGIProxyMiddleware
    app.register_blueprint(app_views)

    app = WsgiToAsgi(app)

    # Run the Flask app
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
