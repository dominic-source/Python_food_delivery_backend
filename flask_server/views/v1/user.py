from flask_server.views.v1 import app_views

@app_views.route('/', strict_slashes=False)
def user():
  """Test the user"""
  return 'i dey work o chinonso'
