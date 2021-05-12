from datetime import datetime
from config import db, ma


class Training(db.Model):
    __tablename__ = "training"
    training_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class TrainingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Training
        sqla_session = db.session
        load_instance = True