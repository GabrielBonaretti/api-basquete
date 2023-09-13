import requests
import json

with open('db.json') as db:
    teams = json.load(db)

class Request:
    def __init__(self):
        self.url = "https://api-basketball.p.rapidapi.com/teams"
        self.headers = {
            "X-RapidAPI-Key": "d5dc38e563msh6d6ba9b0f6ec2a9p129756jsnaa5724b46b3a",
            "X-RapidAPI-Host": "api-basketball.p.rapidapi.com"
        }


class getTeam(Request):
    def __init__(self, url, headers, query_string):
        super().__init__(url, headers)
        self.query_string = query_string

    def getTeamInformation(self):
        response = requests.get(self.url, headers=self.headers, params=self.query_string)

        id_team = response["response"][0]["id"]
        name_team = response["response"][0]["name"]
        code_country = response["response"][0]["country"]["code"]

        if code_country == "BR":
            id_legue = 26
        elif code_country == "US":
            id_legue = 12

        return {"id_name": id_team, "name": name_team, "id_legue": id_legue}


class getAnalytics(Request):
    def __init__(self, url, headers, query_string):
        super().__init__(url, headers)
        self.query_string = query_string

    def getAnalyticsTeam(self):
        response = requests.get(self.url, headers=self.headers, params=self.query_string)

        print(response.json())
