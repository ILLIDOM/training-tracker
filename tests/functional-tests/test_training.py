from src.model.models import Training


def test_training_get(test_client):
    response = test_client.get("/trainings")
    assert response.status_code == 200


def test_a_transaction(db):
    row = db.session.query(Training).get(1)

    # assert row.name == "Pull"

    row.name = 'testing'

    db.session.add(row)
    db.session.commit()

def test_transaction_doesnt_persist(db):
    row = db.session.query(Training).get(1) 
    assert row.name != 'testing'