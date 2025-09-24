from src.data import ping_db

def test_db_ping():
    assert ping_db()
