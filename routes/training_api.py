from flask import (
    Blueprint, 
    Flask, 
    json, 
    request, 
    abort
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
        abort(
            404,
            "Person with Id: {person_id} not found".format(training_id=training_id),
        )

@routes.route("/trainings", methods=["POST"])
def create(training):
    # name = training.get("name")

    # existing_training = (
    #     Training.query.filter(Training.name == name)
    #     .one_or_none()
    # )
    return 1


@routes.route("/trainings/<int:training_id>", methods=["DELETE"])
def delete(training_id):
    return 1