import requests
import json

with open('db.json') as db:
    teams = json.load(db)


class Request:
    def __init__(self):
        self.headers = {
            "X-RapidAPI-Key": "d5dc38e563msh6d6ba9b0f6ec2a9p129756jsnaa5724b46b3a",
            "X-RapidAPI-Host": "api-basketball.p.rapidapi.com"
        }

    def getTeamInformation(self, endpoint, query_string):
        response = requests.get(
            endpoint,
            headers=self.headers,
            params=query_string
        )
       
        response_json = response.json()["response"][0]

        id_team = response_json["id"]
        name_team = response_json["name"]
        code_country = response_json["country"]["code"]

        if code_country == "BR":
            id_legue = 26
        elif code_country == "US":
            id_legue = 12

        return {"id_team": id_team, "name": name_team, "id_legue": id_legue}

    def getAnalyticsTeam(self, endpoint, query_string):
        response = requests.get(
            endpoint,
            headers=self.headers,
            params=query_string
        )

        response_json = response.json()["response"]

        id_team = response_json["team"]["id"]
        name_team = response_json["team"]["name"]

        id_legue = response_json["league"]["id"]
        name_legue = response_json["league"]["name"]

        played = response_json["games"]["played"]["all"]
        wins = response_json["games"]["wins"]["all"]
        lose = response_json["games"]["loses"]["all"]
        points_for_total = response_json["points"]["for"]["total"]
        points_for_average = response_json["points"]["for"]["average"]
        points_against_total = response_json["points"]["against"]["total"]
        points_against_average = response_json["points"]["against"]["average"]

        results_json = {
            "team": {
                "id": id_team,
                "name": name_team,
            },
            "league": {
                "id": id_legue,
                "name": name_legue
            },
            "statistic": {
                "played": played,
                "wins": wins,
                "lose": lose,
                "points_for_total": points_for_total,
                "points_for_avarage": points_for_average,
                "points_against_total": points_against_total,
                "points_against_avarage": points_against_average
            }
        }

        return results_json
