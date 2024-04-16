from flask_server import app, db
from flask_server.views.v1 import app_views

app.register_blueprint(app_views)

with app.app_context():
	db.create_all()

if __name__ == '__main__':
	app.run(port=5000, host='127.0.0.1')
