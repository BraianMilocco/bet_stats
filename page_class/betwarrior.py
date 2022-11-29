import requests
from page_class.base import Base


class BetWarrior(Base):
    def __init__(self):
        self.session_url = "https://auth.shapegamesbwprovince.com/api/session?type=web-betwarrior-province&version=1.0.0"
        base_url = "https://sportsbook-api.shapegamesbwprovince.com/api/event_group_lists/"
        token = self.get_token()
        headers = {
            "authorization": f"Bearer {token}"
        }
        super().__init__(base_url, headers)

    def get_leagues(self, sport, specific_league=None):
        leagues_list = {
            "basketball": [
                {
                    "name":"NBA",
                    "end_url": "standard%3Alevel_type%3Dregion%2Clevel_id%3D1000093652"
                },
                {
                    "name":"LNB",
                    "end_url": "standard%3Alevel_type%3Dleague%2Clevel_id%3D2000050596"
                },
                {
                    "name":"Euroleague",
                    "end_url": "standard%3Alevel_type%3Dregion%2Clevel_id%3D1000093451"
                },
                {
                    "name":"Spain",
                    "end_url": "standard%3Alevel_type%3Dleague%2Clevel_id%3D2010133814"
                }

            ]
        }
        leagues = leagues_list.get(sport, None)
        if leagues and specific_league:
            for league in leagues:
                if league["name"] == specific_league:
                    return [league]
        return leagues

    def get_token(self):
        response = requests.get(self.session_url)
        return response.json().get("session", "")

    @staticmethod
    def fill_start_date_info(data, game):
        data["start-date"] = game["scheduled_start_time"]

    @staticmethod
    def fill_teams_info(data, game):
        data["teams"] = {
            "home": {
                "id": game["participants"]["home"]["id"],
                "name": game["participants"]["home"]["name"]
            },
            "away": {
                "id": game["participants"]["away"]["id"],
                "name": game["participants"]["away"]["name"]
            }
        }

    @staticmethod
    def fill_markets_info(data, game):
        data["markets"] = {
            "odds": {
                "home": game["markets"][0]["outcomes"][0]["current_decimal_odds"],
                "away": game["markets"][0]["outcomes"][1]["current_decimal_odds"]
            }
        }

    @staticmethod
    def fill_id_info(data, game):
        data["id"] = game["id"]

    def get_basketaball_games_info(self, league=None):
        sport = "basketball"
        games = list()
        leagues = self.get_leagues(sport, specific_league=league)
        if not leagues:
            return None

        for league in leagues:
            response = self.get_request_json(extra_url=league["end_url"])

            for day in response:
                if not day.get("date", None):
                    continue
                for game in day["events"]:
                    data = self.get_base_dict(sport, league["name"])
                    self.fill_id_info(data, game)
                    self.fill_start_date_info(data, game)
                    self.fill_teams_info(data, game)
                    self.fill_markets_info(data, game)
                    games.append(data)

        return games
