import os
from config import db
from model.models import Training

TRAINING = [
    {"name": "Push"},
    {"name": "Pull"}
]

if os.path.exists("training.db"):
    os.remove("training.db")

db.create_all()

for training in TRAINING:
    t = Training(name=training.get("name"))
    db.session.add(t)

db.session.commit()