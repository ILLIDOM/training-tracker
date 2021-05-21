import json
from src.model.models import Training
from src import db as _db_flask


def test_a_transaction(db):
    row = db.session.query(Training).get(1)
    row.name = 'hallo'

    db.session.add(row)
    db.session.commit()

def test_transaction_doesnt_persist(session):
    row = session.query(Training).get(1) 
    assert row.name != 'hallo'


def test_training_get(test_client):
    response = test_client.get("/trainings")

    json_data = response.data
    
    training = Training.query.order_by(Training.name).all()

    assert response.status_code == 200


def test_training_get_specific_training(test_client):
    response = test_client.get("/trainings/1")

    row = _db_flask.session.query(Training).get(1)

    data = json.loads(response.get_data(as_text=True))
    
    training = Training.query.filter(
        Training.training_id == 1
    ).one_or_none()

    assert data['name'] == training.name
    assert response.status_code == 200