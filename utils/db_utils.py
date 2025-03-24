import json


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def _saveClubs(listOfClubs):
    with open("clubs.json", "r+") as c:
        c.seek(0)
        json.dump({"clubs": listOfClubs}, c)
        c.truncate()


def updateClubPoint(club_values):
    listOfClubs = loadClubs()
    for club in listOfClubs:
        if club_values["name"] == club["name"]:
            club["points"] = club_values["points"]
    _saveClubs(listOfClubs)


# **********************************************************************


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


def _saveCompetitions(listOfCompetitions):
    with open("competitions.json", "r+") as c:
        c.seek(0)
        json.dump({"competitions": listOfCompetitions}, c)
        c.truncate()


def updateCompetition(competition_values):
    listOfCompetitions = loadCompetitions()
    for competition in listOfCompetitions:
        if competition_values["name"] == competition["name"]:
            competition.update(competition_values)
    _saveCompetitions(listOfCompetitions)
