from utils.db_utils import (
    loadClubs,
    loadCompetitions,
    updateCompetitionPlaces,
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

    original_club.update({"points": "13"})
    original_comp.update({"numberOfPlaces": "25"})
    updateClubPoint(original_club)
    updateCompetitionPlaces(original_comp)

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
    updateClubPoint(original_club)
    updateCompetitionPlaces(original_comp)


def test_should_fail_booking__club_points(client):
    before_clubs = loadClubs()
    before_competitions = loadCompetitions()

    club_name = "Simply Lift"
    competition_name = "Spring Festival"

    original_club = [c for c in before_clubs if c["name"] == club_name][0]
    original_comp = [c for c in before_competitions if c["name"] == competition_name][0]

    original_club_points = original_club["points"]
    original_comp_places = original_comp["numberOfPlaces"]

    original_club.update({"points": "2"})
    original_comp.update({"numberOfPlaces": "25"})
    updateClubPoint(original_club)
    updateCompetitionPlaces(original_comp)

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
    updateClubPoint(original_club)
    updateCompetitionPlaces(original_comp)


def test_should_fail_booking__competitions_places(client):
    before_clubs = loadClubs()
    before_competitions = loadCompetitions()

    club_name = "Simply Lift"
    competition_name = "Spring Festival"

    original_club = [c for c in before_clubs if c["name"] == club_name][0]
    original_comp = [c for c in before_competitions if c["name"] == competition_name][0]

    original_club_points = original_club["points"]
    original_comp_places = original_comp["numberOfPlaces"]

    original_club.update({"points": "13"})
    original_comp.update({"numberOfPlaces": "2"})
    updateClubPoint(original_club)
    updateCompetitionPlaces(original_comp)

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
    updateClubPoint(original_club)
    updateCompetitionPlaces(original_comp)