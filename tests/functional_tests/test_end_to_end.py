import gevent.monkey

gevent.monkey.patch_all()

import random
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils.db_utils import (loadClubs, loadCompetitions, updateClubPoint,
                            updateCompetition)


def test_end_to_end_success(client, init_server):
    clubs = loadClubs()
    competitions = loadCompetitions()

    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000")
    assert "GUDLFT Registration" in driver.title

    email_form = driver.find_element(By.TAG_NAME, "input")
    email = "john@simplylift.co"
    email_form.send_keys(email)
    driver.find_element(By.TAG_NAME, "button").click()
    assert "Invalid credentials." not in driver.find_elements(By.TAG_NAME, "li")

    wait = WebDriverWait(driver, timeout=2)
    wait.until(EC.url_to_be("http://127.0.0.1:5000/welcome"))
    assert "Summary | GUDLFT Registration" in driver.title
    club = [club for club in clubs if club["email"] == email][0]
    point_original_value = int(club["points"])
    points = driver.find_element(By.ID, "points")
    assert points.text == f"Points available: {point_original_value}"

    driver.find_elements(By.LINK_TEXT, "Book Places")[0].click()
    wait.until(
        EC.url_to_be("http://127.0.0.1:5000/book/Spring%20Festival/Simply%20Lift")
    )

    competition = [c for c in competitions if c["name"] == "Spring Festival"][0]
    points = driver.find_element(By.ID, "points")
    assert points.text == f"Places available: {competition['numberOfPlaces']}"

    places_original_value = int(competition["numberOfPlaces"])
    date_original_value = competition["date"]
    later = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")
    competition.update({"date": later})
    updateCompetition(competition)

    places_input = driver.find_element(By.NAME, "places")
    number_of_places = random.randint(1, min(12, places_original_value))
    places_input.send_keys(number_of_places)
    driver.find_element(By.TAG_NAME, "button").click()
    wait.until(EC.url_to_be("http://127.0.0.1:5000/purchasePlaces"))
    assert driver.find_elements(By.TAG_NAME, "li")[0].text == "Great-booking complete!"
    points = driver.find_element(By.ID, "points")
    assert points.text == f"Points available: {point_original_value - number_of_places}"
    places = driver.find_element(By.ID, "places")
    assert places.text == f"Number of Places: {places_original_value - number_of_places}"

    competition.update({"date": date_original_value})
    competition.update({"numberOfPlaces": str(places_original_value)})
    club.update({"points": str(point_original_value)})
    updateCompetition(competition)
    updateClubPoint(club)

    driver.find_elements(By.TAG_NAME, "a")[0].click()
    wait.until(EC.url_to_be("http://127.0.0.1:5000/"))

    driver.quit()


def test_end_to_end_fail(client, init_server):
    clubs = loadClubs()
    competitions = loadCompetitions()

    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000")
    assert "GUDLFT Registration" in driver.title

    email_form = driver.find_element(By.TAG_NAME, "input")
    email = "john@simplylift.co"
    email_form.send_keys(email)
    driver.find_element(By.TAG_NAME, "button").click()
    assert "Invalid credentials." not in driver.find_elements(By.TAG_NAME, "li")

    wait = WebDriverWait(driver, timeout=2)
    wait.until(EC.url_to_be("http://127.0.0.1:5000/welcome"))
    assert "Summary | GUDLFT Registration" in driver.title
    club = [club for club in clubs if club["email"] == email][0]
    point_original_value = int(club["points"])
    points = driver.find_element(By.ID, "points")
    assert points.text == f"Points available: {point_original_value}"

    driver.find_elements(By.LINK_TEXT, "Book Places")[0].click()
    wait.until(
        EC.url_to_be("http://127.0.0.1:5000/book/Spring%20Festival/Simply%20Lift")
    )

    competition = [c for c in competitions if c["name"] == "Spring Festival"][0]
    points = driver.find_element(By.ID, "points")
    assert points.text == f"Places available: {competition['numberOfPlaces']}"

    places_original_value = int(competition["numberOfPlaces"])
    date_original_value = competition["date"]
    later = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")
    competition.update({"date": later})
    updateCompetition(competition)

    places_input = driver.find_element(By.NAME, "places")
    number_of_places = random.randint(1, min(12, places_original_value))
    places_input.send_keys(number_of_places)
    driver.find_element(By.TAG_NAME, "button").click()
    wait.until(EC.url_to_be("http://127.0.0.1:5000/purchasePlaces"))
    assert driver.find_elements(By.TAG_NAME, "li")[0].text == "Great-booking complete!"
    points = driver.find_element(By.ID, "points")
    assert points.text == f"Points available: {point_original_value - number_of_places}"
    places = driver.find_element(By.ID, "places")
    assert places.text == f"Number of Places: {places_original_value - number_of_places}"

    competition.update({"date": date_original_value})
    competition.update({"numberOfPlaces": str(places_original_value)})
    club.update({"points": str(point_original_value)})
    updateCompetition(competition)
    updateClubPoint(club)

    driver.find_elements(By.TAG_NAME, "a")[0].click()
    wait.until(EC.url_to_be("http://127.0.0.1:5000/"))

    driver.quit()