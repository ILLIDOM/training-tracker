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
    training = Training.query.filter(Training.training_id == training_id).one_or_none()

    if training is None:
        abort(404)

    schema = ExerciceSchema()
    new_exercice_json = request.json
    new_exercice = schema.load(new_exercice_json, session=db.session)

    training.exercices.append(new_exercice)
    db.session.commit()

    data = schema.dump(new_exercice)

    return (json.dumps(data), 200, {'content-type': 'application/json'})


@exercice_api.route("/trainings/<int:training_id>/exercices/<int:exercice_id>", methods=["DELETE"])
def delete(training_id, exercice_id):

    exercice = (
        Exercice.query.filter(Training.training_id == training_id)
        .filter(Exercice.exercice_id == exercice_id)
        .one_or_none()
    )

    if exercice is None:
        abort(404)

    db.session.delete(exercice)
    db.session.commit()

    return make_response(
        "Exercice {exercice_id} deleted".format(exercice_id=exercice_id), 200
    )


@exercice_api.route("/trainings/<int:training_id>/exercices/<int:old_exercice_id>", methods=["PUT"])
def update(training_id, old_exercice_id):
    old_exercice = (
        Exercice.query.filter(Training.training_id == training_id)
        .filter(Exercice.exercice_id == old_exercice_id)
        .one_or_none()
    )

    if old_exercice == None:
        abort(404)

    schema = ExerciceSchema()
    new_exercice_json = request.json
    new_exercice = schema.load(new_exercice_json, session=db.session)

    new_exercice.training_id = training_id
    new_exercice.exercice_id = old_exercice_id

    db.session.merge(new_exercice)
    db.session.commit()

    data = schema.dump(new_exercice)

    return (json.dumps(data), 201, {'content-type': 'application/json'})


@exercice_api.errorhandler(404)
def not_found(error):
    return make_response(json.jsonify({'error': 'Exercice Not found'}), 404)