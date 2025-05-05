from utils.db_utils import loadClubs
import re


def test_points_display(client):
    response = client.post(
        "/showSummary", data={"email": "john@simplylift.co"}, follow_redirects=True
    )
    assert response.status_code == 200
    assert "Welcome, john@simplylift.co" in response.data.decode()

    print(repr(response.data.decode()))

    for club in loadClubs():
        print(club["name"] + ": " + club["points"])
        pattern = rf"<li>\n\s+{re.escape(club["name"])}<br\s+\/>\n\s+Points:\s+{club["points"]}\n\s+<\/li>"
        # pattern = rf"<li>\n\s+{re.escape(club["name"])}<br\s+\/>\n\s+Points:\s+13\n\s+<\/li>"
        # pattern = rf"<li>\n\s+{re.escape(club["name"])}<br\s+\/>\n\s+Points:\s+10\n\s+<\/li>"
        assert re.search(pattern, response.data.decode())
        break
        # assert False
