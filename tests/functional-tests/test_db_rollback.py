from src.model.models import Training


def test_a_transaction(db):
    row = db.session.query(Training).get(1)
    row.name = 'hallo'

    db.session.add(row)
    db.session.commit()

def test_transaction_doesnt_persist(session):
    row = session.query(Training).get(1)
    assert row.name != 'hallo'