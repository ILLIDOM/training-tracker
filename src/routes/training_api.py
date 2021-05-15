from flask import (
    Blueprint,
    Flask,
    json,
    request,
    abort,
    make_response
)

from flask.globals import session
from src import db

from src.model.models import (
    Training,
    TrainingSchema,
    Exercice
)

training_api = Blueprint("training_api", __name__)


@training_api.route("/trainings", methods=["GET"])
def read_all():
    training = Training.query.order_by(Training.name).all()

    training_schema = TrainingSchema(many=True)
    result = training_schema.dump(training)
    return (json.dumps(result), 200, {'content-type': 'application/json'})


@training_api.route("/trainings/<int:training_id>", methods=["GET"])
def read(training_id):
    training = (
        Training.query.filter(Training.training_id == training_id)
        .outerjoin(Exercice)
        .one_or_none()
    )
    if training is not None:
        training_schema = TrainingSchema()
        data = training_schema.dump(training)
        return (json.dumps(data), 200, {'content-type': 'application/json'})

    else:
        abort(404)


@training_api.route("/trainings", methods=["POST"])
def create():
    new_training_json = request.json
    schema = TrainingSchema()
    new_training = schema.load(new_training_json, session=db.session)

    db.session.add(new_training)
    db.session.commit()

    data = schema.dump(new_training)

    return (json.dumps(data), 201, {'content-type': 'application/json'})


@training_api.route("/trainings/<int:old_training_id>", methods=["PUT"])
def update(old_training_id):
    old_training = Training.query.filter(
        Training.training_id == old_training_id
    ).one_or_none()

    if old_training is None:
        abort(404)

    new_training_json = request.json
    schema = TrainingSchema()
    new_training = schema.load(new_training_json, session=db.session)
    new_training.training_id = old_training_id

    db.session.merge(new_training)
    db.session.commit()

    data = schema.dump(new_training)

    return (json.dumps(data), 201, {'content-type': 'application/json'})


@training_api.route("/trainings/<int:training_id>", methods=["DELETE"])
def delete(training_id):
    training = Training.query.filter(
        Training.training_id == training_id
    ).one_or_none()

    if training == None:
        abort(404)

    db.session.delete(training)
    db.session.commit()

    return make_response(
        "Training {training_id} deleted".format(training_id=training_id), 200
    )


@training_api.errorhandler(404)
def not_found(error):
    return make_response(json.jsonify({'error': 'Training Not found'}), 404)