from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(5, 15)
    host = "http://localhost:5000"

    def on_start(self):
        self.client.post(
            "/showSummary",
            {
                "email": "john@simplylift.co",
            },
        )

    @task
    def display_purchase_form(self):
        self.client.get(
            "/book/Spring%20Festival/Simply%20Lift",
        )

    @task
    def purchase_places(self):
        data = {
            "club": "Simply Lift",
            "competition": "Spring Festival",
            "places": 3,
        }
        self.client.post(
            "/purchasePlaces",
            data=data,
        )
