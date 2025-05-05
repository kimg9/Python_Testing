import os

import pytest

from server import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
def test_db():
    os.rename("clubs.json", "real.clubs.json")
    os.rename("competitions.json", "real.competitions.json")
    os.rename("test_clubs.json", "clubs.json")
    os.rename("test_competitions.json", "competitions.json")
    yield
    os.rename("clubs.json", "test_clubs.json")
    os.rename("competitions.json", "test_competitions.json")
    os.rename("real.clubs.json", "clubs.json")
    os.rename("real.competitions.json", "competitions.json")
