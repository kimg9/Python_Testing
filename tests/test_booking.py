from utils.db_utils import (
    loadClubs,
    loadCompetitions,
    updateCompetition,
    updateClubPoint,
)


def test_should_be_able_to_book(client):
    before_clubs = loadClubs()
    before_competitions = loadCompetitions()

    club_name = "Simply Lift"
    competition_name = "Spring Festival"

    original_club = [c for c in before_clubs if c["name"] == club_name][0]
    original_comp = [c for c in before_competitions if c["name"] == competition_name][0]

    original_club_points = original_club["points"]
    original_comp_places = original_comp["numberOfPlaces"]
    original_comp_date = original_comp["date"]

    original_club.update({"points": "13"})
    original_comp.update({"numberOfPlaces": "25"})
    original_comp.update({"date": "2050-03-27 10:00:00"})
    updateClubPoint(original_club)
    updateCompetition(original_comp)

    data = {
        "club": original_club["name"],
        "competition": original_comp["name"],
        "places": 3,
    }
    response = client.post("/purchasePlaces", data=data, follow_redirects=True)

    assert response.status_code == 200
    assert "Great-booking complete!" in response.data.decode()

    after_clubs = loadClubs()
    after_competitions = loadCompetitions()

    for c in after_clubs:
        if c["name"] == club_name:
            assert c["points"] == "10"

    for c in after_competitions:
        if c["name"] == competition_name:
            assert c["numberOfPlaces"] == "22"

    original_club.update({"points": original_club_points})
    original_comp.update({"numberOfPlaces": original_comp_places})
    original_comp.update({"date": original_comp_date})
    updateClubPoint(original_club)
    updateCompetition(original_comp)


def test_should_fail_booking__club_points(client):
    before_clubs = loadClubs()
    before_competitions = loadCompetitions()

    club_name = "Simply Lift"
    competition_name = "Spring Festival"

    original_club = [c for c in before_clubs if c["name"] == club_name][0]
    original_comp = [c for c in before_competitions if c["name"] == competition_name][0]

    original_club_points = original_club["points"]
    original_comp_places = original_comp["numberOfPlaces"]
    original_comp_date = original_comp["date"]

    original_club.update({"points": "2"})
    original_comp.update({"numberOfPlaces": "25"})
    original_comp.update({"date": "2050-03-27 10:00:00"})
    updateClubPoint(original_club)
    updateCompetition(original_comp)

    data = {
        "club": original_club["name"],
        "competition": original_comp["name"],
        "places": 3,
    }
    response = client.post("/purchasePlaces", data=data, follow_redirects=True)

    assert response.status_code == 200
    assert not "Great-booking complete!" in response.data.decode()
    assert (
        "You don&#39;t have enough points to book this many places."
        in response.data.decode()
    )

    after_clubs = loadClubs()
    after_competitions = loadCompetitions()

    for c in after_clubs:
        if c["name"] == club_name:
            assert c["points"] == "2"

    for c in after_competitions:
        if c["name"] == competition_name:
            assert c["numberOfPlaces"] == "25"

    original_club.update({"points": original_club_points})
    original_comp.update({"numberOfPlaces": original_comp_places})
    original_comp.update({"date": original_comp_date})
    updateClubPoint(original_club)
    updateCompetition(original_comp)


def test_should_fail_booking__competitions_places(client):
    before_clubs = loadClubs()
    before_competitions = loadCompetitions()

    club_name = "Simply Lift"
    competition_name = "Spring Festival"

    original_club = [c for c in before_clubs if c["name"] == club_name][0]
    original_comp = [c for c in before_competitions if c["name"] == competition_name][0]

    original_club_points = original_club["points"]
    original_comp_places = original_comp["numberOfPlaces"]
    original_comp_date = original_comp["date"]

    original_club.update({"points": "13"})
    original_comp.update({"numberOfPlaces": "2"})
    original_comp.update({"date": "2050-03-27 10:00:00"})
    updateClubPoint(original_club)
    updateCompetition(original_comp)

    data = {
        "club": original_club["name"],
        "competition": original_comp["name"],
        "places": 3,
    }
    response = client.post("/purchasePlaces", data=data, follow_redirects=True)

    assert response.status_code == 200
    assert not "Great-booking complete!" in response.data.decode()
    assert "The chosen number of places exceeds capacity." in response.data.decode()

    after_clubs = loadClubs()
    after_competitions = loadCompetitions()

    for c in after_clubs:
        if c["name"] == club_name:
            assert c["points"] == "13"

    for c in after_competitions:
        if c["name"] == competition_name:
            assert c["numberOfPlaces"] == "2"

    original_club.update({"points": original_club_points})
    original_comp.update({"numberOfPlaces": original_comp_places})
    original_comp.update({"date": original_comp_date})
    updateClubPoint(original_club)
    updateCompetition(original_comp)


def test_should_fail_booking__maximum_12_places_at_once(client):
    before_clubs = loadClubs()
    before_competitions = loadCompetitions()

    club_name = "Simply Lift"
    competition_name = "Spring Festival"

    original_club = [c for c in before_clubs if c["name"] == club_name][0]
    original_comp = [c for c in before_competitions if c["name"] == competition_name][0]

    original_club_points = original_club["points"]
    original_comp_places = original_comp["numberOfPlaces"]
    original_comp_date = original_comp["date"]

    original_club.update({"points": "13"})
    original_comp.update({"numberOfPlaces": "25"})
    original_comp.update({"date": "2050-03-27 10:00:00"})
    updateClubPoint(original_club)
    updateCompetition(original_comp)

    data = {
        "club": original_club["name"],
        "competition": original_comp["name"],
        "places": 13,
    }
    response = client.post("/purchasePlaces", data=data, follow_redirects=True)

    assert response.status_code == 200
    assert not "Great-booking complete!" in response.data.decode()
    assert "You cannot book more than 12 places at once." in response.data.decode()

    after_clubs = loadClubs()
    after_competitions = loadCompetitions()

    for c in after_clubs:
        if c["name"] == club_name:
            assert c["points"] == "13"

    for c in after_competitions:
        if c["name"] == competition_name:
            assert c["numberOfPlaces"] == "25"

    original_club.update({"points": original_club_points})
    original_comp.update({"numberOfPlaces": original_comp_places})
    original_comp.update({"date": original_comp_date})
    updateClubPoint(original_club)
    updateCompetition(original_comp)


def test_should_fail_booking__outdated_competition(client):
    before_clubs = loadClubs()
    before_competitions = loadCompetitions()

    club_name = "Simply Lift"
    competition_name = "Spring Festival"

    original_club = [c for c in before_clubs if c["name"] == club_name][0]
    original_comp = [c for c in before_competitions if c["name"] == competition_name][0]

    original_comp_date = original_comp["date"]

    original_comp.update({"date": "2020-03-27 10:00:00"})
    updateCompetition(original_comp)

    data = {
        "club": original_club["name"],
        "competition": original_comp["name"],
        "places": 13,
    }
    response = client.post("/purchasePlaces", data=data, follow_redirects=True)

    assert response.status_code == 200
    assert not "Great-booking complete!" in response.data.decode()
    assert (
        "This competition has already happened. You cannot book places for an outdated competition."
        in response.data.decode()
    )

    original_comp.update({"date": original_comp_date})
    updateCompetition(original_comp)
