from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

#######################
#### Configuration ####
#######################

# Create the instances of the Flask extensions (flask-sqlalchemy, flask-login, etc.) in
# the global scope, but without any arguments passed in.  These instances are not attached
# to the application at this point.

db = SQLAlchemy()
ma = Marshmallow()


######################################
#### Application Factory Function ####
######################################

def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    initialize_extensions(app)
    register_blueprints(app)
    return app


##########################
#### Helper Functions ####
##########################

def initialize_extensions(app):
    db.init_app(app)
    ma.init_app(app)


def register_blueprints(app):
    from src.routes.training_api import training_api
    from src.routes.exercice_api import exercice_api
    from src.routes.set_api import set_api
    from src.routes.index import routes

    app.register_blueprint(training_api)
    app.register_blueprint(exercice_api)
    app.register_blueprint(set_api)
    app.register_blueprint(routes)