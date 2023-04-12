from api.v1.views import app_views

@app_views.route('/status')
def index():
  return '{status: "OK"}'
