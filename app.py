from routes import *
import config
from routes.training_api import training_api
from routes.exercice_api import exercice_api
from routes.set_api import set_api


app = config.app

app.register_blueprint(training_api)
app.register_blueprint(exercice_api)
app.register_blueprint(set_api)

@app.route("/")
def index():
    return ("Hallo")

if __name__ == '__main__':
    app.run(debug=True)