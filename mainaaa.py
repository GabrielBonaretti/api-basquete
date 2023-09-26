import json
from models import Team
from request import Request
from fastapi import FastAPI, HTTPException, status, Response, Path
import requests

# get value to file db.json
with open('db.json') as db:
    teams = json.load(db)

# create app FASTAPI
app = FastAPI()

PREFIX_API_BASQUETE: str = '/api/v1/basquete'
PREFIX_API_FUTEBOL: str = '/api/v1/futebol'

# GET

@app.get(PREFIX_API_BASQUETE + "/teams")
async def get_all_teams():
    '''
    getting all teams in file db.json      
    '''
    return teams


@app.get(PREFIX_API_BASQUETE + "/teams/id/{team_id}")
async def get_team_id(team_id: str):
    '''
    getting one teams in file db.json by your id      
    '''
    try:
        team = teams[team_id]
        return {"message": team}
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Team not found!')


@app.get(PREFIX_API_BASQUETE + "/teams/name/{team_name}")
async def get_team_name(team_name: str):
    '''
    getting one teams in file db.json by this key value "name"      
    '''
    try:
        # goes through all teams
        for key in teams:
            # transforms the string key value "name" to everything lowercase and without spaces
            name_team = teams[key]["name"].lower().replace(" ", "")

            # transforms the string param to everything lowercase and without spaces
            param_team = team_name.lower().replace(" ", "")

            # verify if the param have in name of team
            if param_team in name_team:
                return {"message": teams[key]}

    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Team not found!')


@app.get(PREFIX_API_BASQUETE + "/teams/legue/{legue_name}")
async def get_all_legue(legue_name: str):
    '''
    getting all teams that have in one specif league in file db.json by this key value "name"      
    '''

    # the list that will contain the teams
    teams_legue = []

    try:
        # goes through all teams
        for key in teams:
            # transforms the string key value "league" to everything lowercase and without spaces
            legue_team = teams[key]["legue"].lower()

            # transforms the string param to everything lowercase and without spaces
            param_legue = legue_name.lower().replace(" ", "")

            # verify if the param is equal the league team, if true. Append in list
            if param_legue == legue_team:
                teams_legue.append(teams[key])

        return {"message": teams_legue}

    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Team not found!')


@app.get(PREFIX_API_BASQUETE + "/teams/analytics/")
async def get_all_legue(team_name: str, season: str):
    '''
    from the "team_name" and "season" parameters. This function takes data from a team in a season. 
    This is done in 3 steps. 
        1st: It checks if the team requested in the parameter is in the json file, if it doesn't have it, it returns 404. 
        2nd: If it does, it consumes a basketball api that returns the id of the league the team plays in and the id of the team researched. 
        3rd: With the information from the previous request, it makes another request to discover the team's data for the specific season.
    Finally, it returns a json with all the team's data.

    *requests are separated into a class, which has the request header as attributes. And there are two methods, one for each request*
    '''

    #
    name_correct = None
    have_database = False

    # goes through all teams
    for key in teams:
        # transforms the string key value "name" to everything lowercase and without spaces
        name_team = teams[key]["name"].lower().replace(" ", "")

        # transforms the string param to everything lowercase and without spaces
        param_team = team_name.lower().replace(" ", "")

        # verify if the param have in name of team. 
        if param_team in name_team:
            have_database = True
            name_correct = teams[key]["name"]

    # if it is not in the db it returns a 404 error
    if not have_database:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Team not found!')

    try:
        # set the queries to the first request
        params = {"search": name_correct}

        # creates the request object
        request_team = Request()

        # returns the request times values
        team = request_team.getTeamInformation(
            endpoint="https://api-basketball.p.rapidapi.com/teams",
            query_string=params
        )

        # set the queries to the second request
        params_statistics = {
            "season": season,
            "league": team["id_legue"],
            "team": team["id_team"]
        }

        # returns the request times statics value
        statistics = request_team.getAnalyticsTeam(
            endpoint="https://api-basketball.p.rapidapi.com/statistics",
            query_string=params_statistics
        )

        if statistics == None or statistics["league"]["id"] == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Season not found!')

        return {"message": statistics}

    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Team not found!')


@app.get(PREFIX_API_FUTEBOL + "/teams")
async def get_all_teams_futebol():
    '''
    getting all teams in  API diego     
    '''
    reqUrl = "http://10.21.58.247:8001/api/v1/teams/"
    response = requests.get(reqUrl, data="",  headers={})
    teams = response.json()
    return teams

# POST


@app.post(PREFIX_API_BASQUETE + "/teams/add")
async def post_team(team: Team):
    '''
    Create a new team with the name and league model. And the key is all teams plus 1
    '''

    id = len(teams) + 1
    if id not in teams:
        teams[id] = team
        return team, Response(status_code=status.HTTP_201_CREATED)
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'The team with id {id} already exists!')


# PUT

@app.put(PREFIX_API_BASQUETE + '/teams/change/{team_id}')
async def put_team(team_id: str, team: Team):
    '''
    Update the team body according to the team and league model, and the id, passed through the parameter
    '''
    if team_id in teams:
        teams[team_id] = team
        return team
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Team not found!')

# DELETE


@app.delete(PREFIX_API_BASQUETE + "/teams/delete/{team_id}")
async def delete_team(team_id: str):
    '''
    Delete the team according to the id passed in the parameters
    '''
    if team_id in teams:
        del teams[team_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='Team not found!')


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host="0.0.0.0", port=8001,
                log_level="info", reload=True)
