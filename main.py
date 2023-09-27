import json
from models import Team, League
from request import Request
from fastapi import FastAPI, HTTPException, status, Response, Path
from typing import Optional
import requests

from bancoDeDados import listar_times, buscar, listar_ligas, listar_times_liga, inserir_liga, upadate_ligas, delete, inserir_time, upadate_times

# create app FASTAPI
app = FastAPI()

PREFIX_API_BASQUETE: str = '/api/v1/basquete'
PREFIX_API_FUTEBOL: str = '/api/v1/futebol'

# Teams

# GET

@app.get(PREFIX_API_BASQUETE + "/teams")
async def get_all_teams():
    '''
    getting all teams in file db.json      
    '''
    lista_times = listar_times()

    return lista_times

@app.get(PREFIX_API_BASQUETE + "/teams/search/")
async def get_team(team_id: Optional[str] = None, team_name: Optional[str] = None):

    if team_id:
        team = buscar(id=team_id, table='times_de_basquete')
    elif team_name:
        team = buscar(nome=team_name, table='times_de_basquete')
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='The two fields query are empty')

    if team != None or team != []:
        return team
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Team not found!')

@app.get(PREFIX_API_BASQUETE + "/teams/analytics/")
async def get_analytics(league_name: str, season: str):
    '''
    from the "league_name" and "season" parameters. This function takes data from a team in a season. 
    This is done in 3 steps. 
        1st: It checks if the team requested in the parameter is in the json file, if it doesn't have it, it returns 404. 
        2nd: If it does, it consumes a basketball api that returns the id of the league the team plays in and the id of the team researched. 
        3rd: With the information from the previous request, it makes another request to discover the team's data for the specific season.
    Finally, it returns a json with all the team's data.

    *requests are separated into a class, which has the request header as attributes. And there are two methods, one for each request*
    '''

    #
    leagues_name = buscar_nome(league_name)
    
    # if it is not in the db it returns a 404 error
    if leagues_name == None or leagues_name == []:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Team not found!')

    params = {"search": leagues_name[0][2]}
    
    try:
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

    create = inserir_time(team)
    
    if create:
        return Response(status_code=status.HTTP_201_CREATED)
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'The team with id {league.id} already exists!')


# PUT

@app.put(PREFIX_API_BASQUETE + '/teams/change')
async def put_team(team: Team):
    '''
    Update the league body according to the league and league model, and the id, passed through the parameter
    '''
    update = upadate_times(team)

    if update:
        return team
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=F'League not found!')

# DELETE

@app.delete(PREFIX_API_BASQUETE + '/teams/remove')
async def del_team(team_id: int):
    '''
    Update the league body according to the league and league model, and the id, passed through the parameter
    '''
    
    deleted = delete(table='times_de_basquete', id=team_id)
    
    if deleted:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'league not found!')


# Legues

# GET

@app.get(PREFIX_API_BASQUETE + "/leagues")
async def get_all_leagues():
    '''
    getting all teams in file db.json      
    '''
    lista_ligas = listar_ligas()

    return lista_ligas

@app.get(PREFIX_API_BASQUETE + "/leagues/search/")
async def get_league(league_id: Optional[str] = None, league_name: Optional[str] = None):

    if league_id:
        league = buscar(id=league_id, table='ligas_de_basquete')
    elif league_name:
        league = buscar(nome=league_name, table='ligas_de_basquete')
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='The two fields query are empty')

    if league != None or league != []:
        return league
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='League not found!')

@app.get(PREFIX_API_BASQUETE + "/leagues/teams")
async def get_league_name(league_id: Optional[str] = None, league_name: Optional[str] = None):
    if league_id == None and league_name == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='The two query are empty!')
    
    if league_id != None:
        lista_times = listar_times_liga(league_id, 'id')
    elif league_name != None:
        lista_times = listar_times_liga(league_name, 'name')

    if lista_times == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='League not found!')

    return lista_times
    
# POST

@app.post(PREFIX_API_BASQUETE + "/leagues/add")
async def post_league(league: League):
    '''
    Create a new team with the name and league model. And the key is all teams plus 1
    '''

    create = inserir_liga(league)
    
    if create:
        return Response(status_code=status.HTTP_201_CREATED)
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'The team with id {league.id} already exists!')


# PUT

@app.put(PREFIX_API_BASQUETE + '/leagues/change')
async def put_league(league: League):
    '''
    Update the league body according to the league and league model, and the id, passed through the parameter
    '''
    update = upadate_ligas(league)

    if update:
        return league
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=F'League not found!')

# DELETE

@app.delete(PREFIX_API_BASQUETE + '/leagues/remove')
async def del_league(league_id: int):
    '''
    Update the league body according to the league and league model, and the id, passed through the parameter
    '''
    
    deleted = delete(table='ligas_de_basquete', id=league_id)
    
    if deleted:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'league not found!')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host="127.0.0.1", port=8011, log_level="info", reload=True)

