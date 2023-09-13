import json

from fastapi import FastAPI, HTTPException, status, Response, Path
from models import Team

with open('db.json') as db:
    teams = json.load(db)


app = FastAPI()

# GET

@app.get("/teams")
async def get_all_teams():
    return teams


@app.get("/teams/id/{team_id}")
async def get_team_id(team_id: str):
    try:
        team = teams[team_id]
        return {"message": team}
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Team not found!')


@app.get("/teams/name/{team_name}")
async def get_team_name(team_name: str):
    try:
        for key in teams:
            # nome do time no json
            name_team = teams[key]["name"].lower().replace(" ", "")

            # nome do time no parametro
            param_team = team_name.lower().replace(" ", "")

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
    try:
        ...
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
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'The team with id {id} already exists!')


# PUT

@app.put('/teams/change/{team_id}')
async def put_team(team_id: str, team: Team):
    if team_id in teams:
        teams[team_id] = team
        return team
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Team not found!')

# DELETE

@app.delete("/teams/delete/{team_id}")
async def delete_team(team_id: str):
    if team_id in teams:
        del teams[team_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT) 
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Team not found!')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host='127.0.0.1', port=8000,
                log_level="info", reload=True)
