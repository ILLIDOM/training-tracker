import os
from src import db
from src.model.models import Training, Exercice, Set
from src import create_app

app = create_app("flask.cfg")
app.app_context().push()

TRAINING = [
    {
        "name": "Pull",
        "exercices": [
            {
                "exercice_name": "Pull Ups",
                "sets": [
                    {
                        "number": 1,
                        "weight": 0,
                        "reps": 9
                    },
                    {
                        "number": 2,
                        "weight": 0,
                        "reps": 7
                    }
                ]
            },
            {
                "exercice_name": "Rowing",
                "sets": [
                    {
                        "number": 1,
                        "weight": 50.25,
                        "reps": 8
                    },
                    {
                        "number": 2,
                        "weight": 50.25,
                        "reps": 8
                    }
                ]
            }
        ]
    },
    {
        "name": "Push",
        "exercices": [
            {
                "exercice_name": "Push Ups",
                "sets": [
                    {
                        "number": 1,
                        "weight": 0,
                        "reps": 20
                    },
                    {
                        "number": 2,
                        "weight": 0,
                        "reps": 15
                    }
                ]
            },
            {
                "exercice_name": "Dips",
                "sets": [
                    {
                        "number": 1,
                        "weight": 5.67,
                        "reps": 12
                    },
                    {
                        "number": 2,
                        "weight": 0,
                        "reps": 15
                    }
                ]
            }
        ]
    }
]

if os.path.exists("training.db"):
    os.remove("training.db")

db.create_all()

for training in TRAINING:
    t = Training(name=training.get("name"))

    for exercice in training.get("exercices"):

        exercice_name = exercice.get("exercice_name")
        exercice_obj = Exercice(exercice_name = exercice_name)
        t.exercices.append(exercice_obj)
        
        for set in exercice.get("sets"):
            exercice_obj.sets.append(
                Set(
                number=set.get("number"),
                weight = set.get("weight"),
                reps = set.get("reps")
            ))

    db.session.add(t)

db.session.commit()