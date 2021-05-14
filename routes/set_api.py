from flask import (
    Blueprint,
    Flask,
    json,
    request,
    abort,
    make_response
)

from flask.globals import session
from config import db

from model.models import (
    Training,
    TrainingSchema,
    Exercice,
    ExerciceSchema,
    Set,
    SetSchema
)

set_api = Blueprint("set_api", __name__)


@set_api.route("/exercices/<int:exercice_id>/sets", methods=["GET"])
def read_all(exercice_id):
    set = (
        Set.query.join(Exercice, Exercice.exercice_id == Set.exercice_id)
        .filter(Exercice.exercice_id == exercice_id)
        .all()
    )

    set_schema = SetSchema(many=True)
    result = set_schema.dump(set)
    return (json.dumps(result), 200, {'content-type': 'application/json'})


@set_api.route("/exercices/<int:exercice_id>/sets/<int:set_id>", methods=["GET"])
def read(exercice_id, set_id):
    set = (
        Set.query.join(Exercice, Exercice.exercice_id == Set.exercice_id)
        .filter(Exercice.exercice_id == exercice_id)
        .filter(Set.set_id == set_id)
        .one_or_none()
    )

    if set is None:
        abort(404)

    set_schema = SetSchema()
    result = set_schema.dump(set)

    return (json.dumps(result), 200, {'content-type': 'application/json'})


@set_api.route("/exercices/<int:exercice_id>/sets", methods=["POST"])
def create(exercice_id):
    exercice = (
        Exercice.query.filter(Exercice.exercice_id == exercice_id)
        .one_or_none()
    )

    if exercice == None:
        abort(404)

    schema = SetSchema()
    new_set_json = request.json
    new_set = schema.load(new_set_json, session=db.session)

    exercice.sets.append(new_set)
    db.session.commit()

    data = schema.dump(new_set)

    return (json.dumps(data), 200, {'content-type': 'application/json'})


@set_api.route("/exercices/<int:exercice_id>/sets/<int:set_id>", methods=["DELETE"])
def delete(exercice_id, set_id):
    set = (
        Set.query.filter(Set.set_id == set_id)
        .one_or_none()
    )

    if set is None:
        abort(404)

    db.session.delete(set)
    db.session.commit()

    return make_response(
        "Set {set_id} deleted".format(set_id = set_id), 200
    )


@set_api.route("/exercices/<int:exercice_id>/sets/<int:old_set_id>", methods=["PUT"])
def update(exercice_id, old_set_id):
    old_set = (
        Set.query.filter(Set.set_id == old_set_id)
        .one_or_none()
    )

    if old_set is None:
        abort(404)

    schema = SetSchema()
    new_set_json = request.json
    new_set = schema.load(new_set_json, session=db.session)

    new_set.exercice_id = exercice_id
    new_set.set_id = old_set_id

    db.session.merge(new_set)
    db.session.commit()

    data = schema.dump(new_set)

    return (json.dumps(data), 201, {'content-type': 'application/json'})


@set_api.errorhandler(404)
def not_found(error):
    return make_response(json.jsonify({'error': 'Set Not found'}), 404)