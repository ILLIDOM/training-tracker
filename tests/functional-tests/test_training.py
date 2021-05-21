import json, datetime

from src.model.models import Training
from src import db as _db_flask


def test_training_get(test_client):
    response = test_client.get("/trainings")

    data = json.loads(response.get_data(as_text=True))
    training = Training.query.order_by(Training.name).all()

    assert len(data) == len(training)
    assert response.status_code == 200


def test_training_get_specific_training(test_client):
    response = test_client.get("/trainings/1")

    data = json.loads(response.get_data(as_text=True))

    training = Training.query.filter(
        Training.training_id == 1
    ).one_or_none()

    assert data['name'] == training.name
    assert response.status_code == 200


def test_training_post(test_client):
    response = test_client.post('/trainings', json={
        'name': 'New Training'
    })

    json_data = response.get_json()

    assert json_data['training_id'] == 3
    assert json_data['name'] == 'New Training'
    assert len(json_data['exercices']) == 0


def test_training_update_1(test_client):
    old_training = Training.query.filter(
        Training.training_id == 1
    ).one_or_none()
    
    old_id = old_training.training_id
    old_timestamp = old_training.timestamp
    old_timestamp_json = json.dumps(old_timestamp, default=str)

    response = test_client.put('trainings/1', json={
        'name': 'Back Workout'
    })

    json_data = response.get_json()
    new_datetime_json = json_data['timestamp']

    new_datetime = datetime.datetime.strptime(new_datetime_json, '%Y-%m-%dT%H:%M:%S.%f')

    assert json_data['training_id'] == old_id
    assert new_datetime > old_timestamp
    assert json_data['name'] == 'Back Workout'
    assert len(json_data['exercices']) == 2


def test_training_delete_1(test_client):
    response = test_client.delete('/trainings/1')

    