import gevent
from locust import events
from locust.env import Environment
from locust.log import setup_logging
from locust.stats import stats_history, stats_printer

from .locustfile import WebsiteUser

setup_logging("INFO")

def test_performance(client, init_server):
    env = Environment(user_classes=[WebsiteUser], events=events)
    runner = env.create_local_runner()
    web_ui = env.create_web_ui("127.0.0.1", 8089)
    env.events.init.fire(environment=env, runner=runner, web_ui=web_ui)
    gevent.spawn(stats_printer(env.stats))
    gevent.spawn(stats_history, env.runner)
    runner.start(6, spawn_rate=1)
    gevent.spawn_later(30, runner.quit)
    runner.greenlet.join()
    web_ui.stop()

    logging = env.stats.get("/showSummary", "POST")
    form_display = env.stats.get("/book/Spring%20Festival/Simply%20Lift", "GET")
    purchase_places_form = env.stats.get("/purchasePlaces", "POST")
    assert 0 < form_display.max_response_time < 5000
    assert 0 < logging.max_response_time < 2000
    assert 0 < purchase_places_form.max_response_time < 2000

    assert env.stats.total.num_failures == 0
