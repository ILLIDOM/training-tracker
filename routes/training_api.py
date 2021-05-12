from flask import (
    Blueprint,
    Flask,
    json,
    request,
    abort,
    make_response
)
from pprint import pprint
from . import routes
from config import db
from model.models import (
    Training,
    TrainingSchema
)


@routes.route("/trainings", methods=["GET"])
def read_all():
    training = Training.query \
        .order_by(Training.name) \
        .all()

    training_schema = TrainingSchema(many=True)
    result = training_schema.dump(training)
    return (json.dumps(result), 200, {'content-type': 'application/json'})


@routes.route("/trainings/<int:training_id>", methods=["GET"])
def read(training_id):
    training = Training.query \
        .filter(Training.training_id == training_id).one_or_none()

    if training is not None:
        training_schema = TrainingSchema()
        data = training_schema.dump(training)
        return (json.dumps(data), 200, {'content-type': 'application/json'})

    else:
        # abort(
        #     404,
        #     "Person with Id: {person_id} not found".format(
        #         training_id=training_id),
        # )
        abort(404)


@routes.route("/trainings", methods=["POST"])
def create():
    new_training_json = request.json
    schema = TrainingSchema()
    new_training = schema.load(new_training_json, session=db.session)

    db.session.add(new_training)
    db.session.commit()

    data = schema.dump(new_training)

    return (json.dumps(data), 201, {'content-type': 'application/json'})


@routes.route("/trainings/<int:training_id>", methods=["PUT"])
def update(old_training_id, new_training):
    return 1



@routes.route("/trainings/<int:training_id>", methods=["DELETE"])
def delete(training_id):
    return 1


@routes.errorhandler(404)
def not_found(error):
    return make_response(json.jsonify({'error': 'Not found'}), 404)