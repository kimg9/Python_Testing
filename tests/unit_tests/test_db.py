from utils.db_utils import (loadClubs, loadCompetitions, updateClubPoint,
                            updateCompetition)


def test_should_load_clubs_data(client):
    clubs = loadClubs()
    if not clubs or not isinstance(clubs, list) and all(isinstance(c, dict) for c in clubs):
        assert False
    assert True


def test_should_load_competitions_data(client):
    competitions = loadCompetitions()
    if not competitions or not isinstance(competitions, list) and all(isinstance(c, dict) for c in competitions):
        assert False
    assert True


def test_should_update_club_points(client):
    club_name = "Simply Lift"
    club = [c for c in loadClubs() if c["name"] == club_name][0]

    club.update({"points": "10"})
    updateClubPoint(club)

    for c in loadClubs():
        if c["name"] == club_name:
            assert c["points"] == "10"


def test_should_update_competitions_places(client):
    competition_name = "Spring Festival"
    comp = [c for c in loadCompetitions() if c["name"] == competition_name][0]

    comp.update({"numberOfPlaces": "12"})
    updateCompetition(comp)

    for c in loadCompetitions():
        if c["name"] == competition_name:
            assert c["numberOfPlaces"] == "12"
