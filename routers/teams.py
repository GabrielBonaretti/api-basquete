from models import Team
from request import Request
from fastapi import HTTPException, Response, status, APIRouter
from typing import Optional
import requests
import json

from bancoDeDados import listar_times, buscar, delete, inserir_time, upadate_times

# create router FASTAPI
router = APIRouter()

PREFIX_API_BASQUETE: str = '/api/v1/basquete'
PREFIX_API_FUTEBOL: str = '/api/v1/futebol'


@router.get(PREFIX_API_BASQUETE + "/teams", tags=['teams'])
async def get_all_teams():
    '''
    getting all teams in file db.json      
    '''
    lista_times = listar_times()

    lista_json = []

    for item in lista_times:
        item_json = {
            "id": item[0],
            "liga_id": item[1],
            "nome": item[2],
        }

        lista_json.append(item_json)
    
    return lista_json


@router.get(PREFIX_API_BASQUETE + "/teams/specific", tags=['teams'])
async def get_team(team_id: Optional[str] = None, team_name: Optional[str] = None):
    """
    
    """

    if team_id:
        team = buscar(id=team_id, table='times_de_basquete')
    elif team_name:
        team = buscar(nome=team_name, table='times_de_basquete')
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='The two fields query are empty')

    if team != None or team != []:

        lista_json = []

        for item in team:
            item_json = {
                "id": item[0],
                "liga_id": item[1],
                "nome": item[2],
            }

            lista_json.append(item_json)
        
        return lista_json

    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Team not found!')


@router.get(PREFIX_API_BASQUETE + "/teams/analytics/", tags=['teams'])
async def get_analytics(team_name: str, season: str):
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
    team_name = buscar(nome=team_name, table='times_de_basquete')
    
    # if it is not in the db it returns a 404 error
    if team_name == None or team_name == []:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Team not found!')

    params = {"search": team_name[0][2]}
    
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

   
@router.get(PREFIX_API_FUTEBOL + "/teams", tags=['teams'])
async def get_all_teams_futebol():
    '''
    getting all teams in  API diego     
    '''
    reqUrl = "http://10.21.58.247:8001/api/v1/teams/"
    response = requests.get(reqUrl, data="",  headers={})
    teams = response.json()
    return teams

# POST


@router.post(PREFIX_API_BASQUETE + "/teams", tags=['teams'])
async def post_team(team: Team):
    '''
    Create a new team with the name and league model. And the key is all teams plus 1
    '''

    create = inserir_time(team)
    
    if create:
        return Response(status_code=status.HTTP_201_CREATED)
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'The team with id {team.id} already exists!')

# PUT


@router.put(PREFIX_API_BASQUETE + '/teams', tags=['teams'])
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


@router.delete(PREFIX_API_BASQUETE + '/teams', tags=['teams'])
async def del_team(team_id: int):
    '''
    Update the league body according to the league and league model, and the id, passed through the parameter
    '''
    
    deleted = delete(table='times_de_basquete', id=team_id)
    
    if deleted:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'league not found!')
