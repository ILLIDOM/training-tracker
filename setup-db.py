import os
from config import db
from model.models import Training, Exercice

TRAINING = [
    {
        "name": "Pull",
        "exercices": [
            ("Pull Ups"),
            ("Rowing"),
        ],
    },
    {
        "name": "Push",
        "exercices": [
            ("Pushups"),
            ("Dips"),
        ],
    },
]

if os.path.exists("training.db"):
    os.remove("training.db")

db.create_all()

for training in TRAINING:
    t = Training(name=training.get("name"))

    for exercice in training.get("exercices"):
        exercice_name = exercice
        t.exercices.append(
            Exercice(
                exercice_name = exercice_name
            )
        )
    db.session.add(t)

db.session.commit()