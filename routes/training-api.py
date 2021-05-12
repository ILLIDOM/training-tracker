from flask import Blueprint, Flask, json, request
from pprint import pprint
from . import routes
from config import db
from model.models import (
    Training,
    TrainingSchema
)


@routes.route("/trainings", methods=["GET"])
def trainings():
    training = Training.query \
        .order_by(Training.name) \
        .all()

    training_schema = TrainingSchema(many=True)
    result = training_schema.dump(training)
    return (json.dumps(result), 200, {'content-type': 'application/json'})


@routes.route("/trainings", methods=["POST"])
def create():
    return 1


@routes.route("/trainings/<int:training_id>", methods=["GET"])
def show(training_id):
    return 1


@routes.route("/trainings/<int:training_id>", methods=["DELETE"])
def delete(training_id):
    return 1