import json
from models import Team
from request import Request
from fastapi import FastAPI, HTTPException, status, Response, Path
from pyngrok import ngrok

# get value to file db.json
with open('db.json') as db:
    teams = json.load(db)

# create app FASTAPI
app = FastAPI()


# GET
@app.get("/teams")
async def get_all_teams():
    '''
    getting all teams in file db.json      
    '''
    return teams


@app.get("/teams/id/{team_id}")
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


@app.get("/teams/name/{team_name}")
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


@app.get("/teams/legue/{legue_name}")
async def get_all_legue(legue_name: str):
    teams_legue = []

    try:
        for key in teams:
            # nome da liga no json
            legue_team = teams[key]["legue"].lower()

            # nome do time no parametro
            param_legue = legue_name.lower().replace(" ", "")

            if param_legue == legue_team:
                teams_legue.append(teams[key])

        return {"message": teams_legue}

    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Team not found!')


@app.get("/teams/analytics/")
async def get_all_legue(team_name: str, season: str):
    name_correct = None
    have_database = False

    for key in teams:
        # nome do time no json
        name_team = teams[key]["name"].lower().replace(" ", "")

        # nome do time no parametro
        param_team = team_name.lower().replace(" ", "")

        if param_team in name_team:
            have_database = True
            name_correct = teams[key]["name"]

    if not have_database:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Team not found!')

    params = {"search": name_correct}

    try:

        request_team = Request()

        team = request_team.getTeamInformation(
            endpoint="https://api-basketball.p.rapidapi.com/teams",
            query_string=params
        )

        params_statistics = {
            "season": season,
            "league": team["id_legue"],
            "team": team["id_team"]
        }

        statistics = request_team.getAnalyticsTeam(
            endpoint="https://api-basketball.p.rapidapi.com/statistics",
            query_string=params_statistics
        )

        return {"message": statistics}

    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Team not found!')


# POST

@app.post("/teams/add")
async def post_team(team: Team):
    id = len(teams) + 1
    if id not in teams:
        teams[id] = team
        return team, Response(status_code=status.HTTP_201_CREATED)
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'The team with id {id} already exists!')


# PUT

@app.put('/teams/change/{team_id}')
async def put_team(team_id: str, team: Team):
    if team_id in teams:
        teams[team_id] = team
        return team
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Team not found!')

# DELETE


@app.delete("/teams/delete/{team_id}")
async def delete_team(team_id: str):
    if team_id in teams:
        del teams[team_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='Team not found!')


if __name__ == '__main__':
    import uvicorn
    
    ngrok_tunnel = ngrok.connect(8000)
    print('Public URL: ', ngrok_tunnel.public_url)
    uvicorn.run(app, port=8000)
    uvicorn.run('main:app', host="0.0.0.0", port=8001, log_level="info", reload=True)

