import json
from models import Team, League
from request import Request
from fastapi import FastAPI, HTTPException, status, Response, Path
from typing import Optional
import requests

from bancoDeDados import listar_times, buscar_id, buscar_nome, listar_ligas, listar_times_liga, inserir_time

# create app FASTAPI
app2 = FastAPI()

PREFIX_API_BASQUETE: str = '/api/v1/basquete'
PREFIX_API_FUTEBOL: str = '/api/v1/futebol'

# Teams

# GET

@app2.get(PREFIX_API_BASQUETE + "/teams")
async def get_all_teams():
    '''
    getting all teams in file db.json      
    '''
    lista_times = listar_times()

    return lista_times


@app2.get(PREFIX_API_BASQUETE + "/teams/id/{team_id}")
async def get_team_id(team_id: str):
    '''
    getting one teams in file db.json by your id      
    '''
    team = buscar_id(team_id, 'times_de_basquete')

    if team != None:
        return team
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Team not found!')


@app2.get(PREFIX_API_BASQUETE + "/teams/name/{league_name}")
async def get_league_name(league_name: str):
    '''
    getting one teams in file db.json by your id      
    '''
    leagues_name = buscar_nome(league_name, 'times_de_basquete')

    if leagues_name != None and leagues_name != []:
        return list(leagues_name)
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Team not found!')


@app2.get(PREFIX_API_BASQUETE + "/teams/analytics/")
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
    name_correct = None
    have_database = False

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

   
@app2.get(PREFIX_API_FUTEBOL + "/teams")
async def get_all_teams_futebol():
    '''
    getting all teams in  API diego     
    '''
    reqUrl = "http://10.21.58.247:8001/api/v1/teams/"
    response = requests.get(reqUrl, data="",  headers={})
    teams = response.json()
    return teams


# Legues

# GET

@app2.get(PREFIX_API_BASQUETE + "/leagues")
async def get_all_leagues():
    '''
    getting all teams in file db.json      
    '''
    lista_ligas = listar_ligas()

    return lista_ligas


@app2.get(PREFIX_API_BASQUETE + "/leagues/id/{leagues_id}")
async def get_league_id(league_id: str):
    '''
    getting one teams in file db.json by your id      
    '''
    league = buscar_id(league_id, 'ligas_de_basquete')

    if league != None:
        return league
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='League not found!')


@app2.get(PREFIX_API_BASQUETE + "/league/name/{league_name}")
async def get_league_name(league_name: str):
    '''
    getting one teams in file db.json by your id      
    '''
    leagues_name = buscar_nome(league_name, 'ligas_de_basquete')

    if leagues_name != None and leagues_name != []:
        return list(leagues_name)
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='League not found!')


@app2.get(PREFIX_API_BASQUETE + "/league/teams")
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

@app2.post(PREFIX_API_BASQUETE + "/league/add")
async def post_team(league: League):
    '''
    Create a new team with the name and league model. And the key is all teams plus 1
    '''

    if league:
        inserir_time(league)
        return Response(status_code=status.HTTP_201_CREATED)
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'The team with id {id} already exists!')


# PUT

@app2.put(PREFIX_API_BASQUETE + '/league/change')
async def put_league(league: League, league_id: Optional[str] = None, league_name: Optional[str] = None):
    '''
    Update the league body according to the league and league model, and the id, passed through the parameter
    '''
    if league and league_id:
        return league
    elif league and league_name:
        return league
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'league not found!')



if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app2', host="127.0.0.1", port=8011, log_level="info", reload=True)

