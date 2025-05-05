from utils.db_utils import (loadClubs, loadCompetitions, updateClubPoint,
                            updateCompetition)


def test_should_be_able_to_book(client):
    club_name = "Simply Lift"
    competition_name = "Spring Festival"

    original_club = [c for c in loadClubs() if c["name"] == club_name][0]
    original_comp = [c for c in loadCompetitions() if c["name"] == competition_name][0]

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

    for c in loadClubs():
        if c["name"] == club_name:
            assert c["points"] == "10"

    for c in loadCompetitions():
        if c["name"] == competition_name:
            assert c["numberOfPlaces"] == "22"


def test_should_fail_booking__club_points(client):
    club_name = "Simply Lift"
    competition_name = "Spring Festival"

    original_club = [c for c in loadClubs() if c["name"] == club_name][0]
    original_comp = [c for c in loadCompetitions() if c["name"] == competition_name][0]

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
    assert "Great-booking complete!" not in response.data.decode()
    assert (
        "You don&#39;t have enough points to book this many places."
        in response.data.decode()
    )

    for c in loadClubs():
        if c["name"] == club_name:
            assert c["points"] == "2"

    for c in loadCompetitions():
        if c["name"] == competition_name:
            assert c["numberOfPlaces"] == "25"


def test_should_fail_booking__competitions_places(client):
    club_name = "Simply Lift"
    competition_name = "Spring Festival"

    original_club = [c for c in loadClubs() if c["name"] == club_name][0]
    original_comp = [c for c in loadCompetitions() if c["name"] == competition_name][0]

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
    assert "Great-booking complete!" not in response.data.decode()
    assert "The chosen number of places exceeds capacity." in response.data.decode()

    for c in loadClubs():
        if c["name"] == club_name:
            assert c["points"] == "13"

    for c in loadCompetitions():
        if c["name"] == competition_name:
            assert c["numberOfPlaces"] == "2"


def test_should_fail_booking__maximum_12_places_at_once(client):
    club_name = "Simply Lift"
    competition_name = "Spring Festival"

    original_club = [c for c in loadClubs() if c["name"] == club_name][0]
    original_comp = [c for c in loadCompetitions() if c["name"] == competition_name][0]

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
    assert "Great-booking complete!" not in response.data.decode()
    assert "You cannot book more than 12 places at once." in response.data.decode()

    for c in loadClubs():
        if c["name"] == club_name:
            assert c["points"] == "13"

    for c in loadCompetitions():
        if c["name"] == competition_name:
            assert c["numberOfPlaces"] == "25"


def test_should_fail_booking__outdated_competition(client):
    club_name = "Simply Lift"
    competition_name = "Spring Festival"

    original_club = [c for c in loadClubs() if c["name"] == club_name][0]
    original_comp = [c for c in loadCompetitions() if c["name"] == competition_name][0]

    original_comp.update({"date": "2020-03-27 10:00:00"})
    updateCompetition(original_comp)

    data = {
        "club": original_club["name"],
        "competition": original_comp["name"],
        "places": 13,
    }
    response = client.post("/purchasePlaces", data=data, follow_redirects=True)

    assert response.status_code == 200
    assert "Great-booking complete!" not in response.data.decode()
    assert (
        "This competition has already happened. You cannot book places for an outdated competition."
        in response.data.decode()
    )
