from utils.db_utils import (
    loadClubs,
    loadCompetitions,
    updateClubPoint,
    updateCompetition,
)


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
    before_clubs = loadClubs()
    club_name = "Simply Lift"
    club = [c for c in before_clubs if c["name"] == club_name][0]
    club_points = club["points"]

    club.update({"points": "10"})
    updateClubPoint(club)

    after_clubs = loadClubs()
    for c in after_clubs:
        if c["name"] == club_name:
            assert c["points"] == "10"

    club.update({"points": club_points})
    updateClubPoint(club)

    after_after_clubs = loadClubs()
    for c in after_after_clubs:
        if c["name"] == club_name:
            assert c["points"] == club_points


def test_should_update_competitions_places(client):
    before_competitions = loadCompetitions()
    competition_name = "Spring Festival"
    comp = [c for c in before_competitions if c["name"] == competition_name][0]
    comp_places = comp["numberOfPlaces"]

    comp.update({"numberOfPlaces": "12"})
    updateCompetition(comp)

    after_competitions = loadCompetitions()
    for c in after_competitions:
        if c["name"] == competition_name:
            assert c["numberOfPlaces"] == "12"

    comp.update({"numberOfPlaces": comp_places})
    updateCompetition(comp)

    after_after_competitions = loadCompetitions()
    for c in after_after_competitions:
        if c["name"] == competition_name:
            assert c["numberOfPlaces"] == comp_places

