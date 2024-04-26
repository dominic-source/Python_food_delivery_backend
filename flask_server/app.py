from flask_server import app, db
from flask_server.views.v1 import app_views

app.register_blueprint(app_views)

with app.app_context():
	db.create_all()


@app.errorhandler(404)
def page_not_found():
    """Handle page not found"""
    return 'This page does not exist', 404

  
if __name__ == '__main__':
	app.run(port=5000, host='127.0.0.1')
