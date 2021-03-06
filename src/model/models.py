from datetime import datetime

from sqlalchemy.orm import backref
from src import db, ma
from marshmallow import fields

class Training(db.Model):

    __tablename__ = "training"

    training_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    exercices = db.relationship(
        'Exercice', 
        backref='training',
        cascade = 'all, delete, delete-orphan',
        single_parent=True,
        order_by = 'desc(Exercice.timestamp)'
    )


class Exercice(db.Model):

    __tablename__ = "exercice"

    exercice_id = db.Column(db.Integer, primary_key=True)
    training_id = db.Column(db.Integer, db.ForeignKey("training.training_id"))
    exercice_name = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    sets = db.relationship(
        'Set',
        backref='exercice',
        cascade='all, delete, delete-orphan',
        single_parent=True,
        order_by = 'asc(Set.number)'
    )


class Set(db.Model):

    __tablename__ = "set"
    
    set_id = db.Column(db.Integer, primary_key=True)
    exercice_id = db.Column(db.Integer, db.ForeignKey("exercice.exercice_id"))
    number = db.Column(db.Integer)
    weight = db.Column(db.Float)
    reps = db.Column(db.Integer)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


# Marshmallow Schemas


class TrainingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Training
        sqla_session = db.session
        include_realationships = True
        load_instance = True
    exercices = fields.Nested('TrainingExerciceSchema', default=[], many=True)


class TrainingExerciceSchema(ma.SQLAlchemyAutoSchema):
    training_id = fields.Int()
    exercice_id = fields.Int()
    exercice_name = fields.Str()
    timestamp = fields.Str()


class ExerciceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Exercice
        sqla_session = db.session
        include_fk = True
        load_instance = True
    training = fields.Nested('ExerciceTrainingSchema', default=None)
    sets = fields.Nested('ExerciceSetSchema', default=[], many=True)


class ExerciceTrainingSchema(ma.SQLAlchemyAutoSchema):
    training_id = fields.Int()
    name = fields.Str()
    timestamp = fields.Str()


class ExerciceSetSchema(ma.SQLAlchemyAutoSchema):
    set_id = fields.Int()
    number = fields.Int()
    weight = fields.Float()
    reps = fields.Int()
    timestamp = fields.Str()


class SetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Set
        sqla_session = db.session
        include_fk = True
        load_instance = True
    exercice = fields.Nested('SetExerciceSchema', default=None)


class SetExerciceSchema(ma.SQLAlchemyAutoSchema):
    exercice_id = fields.Int()
    exercice_name = fields.Str()
    timestamp = fields.Str()