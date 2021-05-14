from flask import (
    Blueprint,
    Flask,
    json,
    request,
    abort,
    make_response
)

from flask.globals import session
# from . import routes
from config import db

from model.models import (
    Training,
    TrainingSchema,
    Exercice,
    ExerciceSchema
)

exercice_api = Blueprint("exercice_api", __name__)

@exercice_api.route("/trainings/<int:training_id>/exercices/<int:exercice_id>", methods=["GET"])
def read_exercice(training_id, exercice_id):
    exercice = (
        Exercice.query.join(Training, Training.training_id == Exercice.training_id)
        .filter(Training.training_id == training_id)
        .filter(Exercice.exercice_id == exercice_id)
        .one_or_none()
    )

    if exercice == None:
        abort(404)

    exercice_schema = ExerciceSchema()
    data = exercice_schema.dump(exercice)
    return (json.dumps(data), 200, {'content-type': 'application/json'})


@exercice_api.route("/trainings/<int:training_id>/exercices", methods=["POST"])
def create(training_id):
    return 1