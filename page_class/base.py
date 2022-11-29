from datetime import datetime
import requests


class Base():

    sports = ["basketball"]

    def __init__(self, url, headers):
        self.base_url = url
        self.headers = headers

    def get_base_dict(self, sport, league):
        return {
            "created_at": datetime.now(),
            "sport": sport,
            "league": league
        }

    def get_request_json(self, extra_url=None):
        url = f"{self.base_url}{extra_url}" if extra_url else self.base_url
        response = requests.get(url, headers=self.headers)
        return response.json()
