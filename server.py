from datetime import datetime

from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)

from utils.db_utils import (loadClubs, loadCompetitions, updateClubPoint,
                            updateCompetition)

app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/welcome")
def welcome():
    club = session.pop("club")
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/showSummary", methods=["POST"])
def showSummary():
    club = [club for club in clubs if club["email"] == request.form["email"]]
    if not club:
        flash("Invalid credentials.")
        return render_template("index.html")
    else:
        session["club"] = club[0]
        return redirect(url_for("welcome"))


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]
    if foundClub and foundCompetition:
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [
        c for c in loadCompetitions() if c["name"] == request.form["competition"]
    ][0]
    club = [c for c in loadClubs() if c["name"] == request.form["club"]][0]
    requestedPlaces = int(request.form["places"])
    updatedNumberOfPlaces = int(competition["numberOfPlaces"]) - requestedPlaces
    updatedPoints = int(club["points"]) - requestedPlaces

    competition_date = datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")
    current_datetime = datetime.now()

    errors = False
    if competition_date < current_datetime:
        flash(
            "This competition has already happened. You cannot book places for an outdated competition."
        )
        return render_template("booking.html", club=club, competition=competition)
    if requestedPlaces > 12:
        flash("You cannot book more than 12 places at once.")
        errors = True
    if updatedPoints < 0:
        flash("You don't have enough points to book this many places.")
        errors = True
    if updatedNumberOfPlaces < 0:
        flash("The chosen number of places exceeds capacity.")
        errors = True

    if errors:
        return render_template("booking.html", club=club, competition=competition)
    else:
        competition.update({"numberOfPlaces": str(updatedNumberOfPlaces)})
        club.update({"points": str(updatedPoints)})
        updateCompetition(competition)
        updateClubPoint(club)
        flash("Great-booking complete!")
        competitions = loadCompetitions()
        return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
