from models import League
from fastapi import HTTPException, Response, status, APIRouter
from typing import Optional

from bancoDeDados import buscar, listar_ligas, listar_times_liga, inserir_liga, upadate_ligas, delete

# create router FASTAPI
router = APIRouter()

PREFIX_API_BASQUETE: str = '/api/v1/basquete'
PREFIX_API_FUTEBOL: str = '/api/v1/futebol'

# Legues

# GET

@router.get(PREFIX_API_BASQUETE + "/leagues", tags=['leagues'])
async def get_all_leagues():
    '''
    getting all leagues in database
    '''

    # get in database
    lista_ligas = listar_ligas()

    # transform to json list
    lista_json = []

    for item in lista_ligas:
        item_json = {
            "id": item[0],
            "nome": item[1],
        }

        lista_json.append(item_json)
    
    return lista_json


@router.get(PREFIX_API_BASQUETE + "/leagues/specific", tags=['leagues'])
async def get_league(league_id: Optional[str] = None, league_name: Optional[str] = None):
    if league_id:
        league = buscar(id=league_id, table='ligas_de_basquete')
    elif league_name:
        league = buscar(nome=league_name, table='ligas_de_basquete')
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='The two fields query are empty')

    if league != None or league != []:
        lista_json = []

        for item in league:
            item_json = {
                "id": item[0],
                "nome": item[1],
            }

            lista_json.append(item_json)
        
        return lista_json
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='League not found!')


@router.get(PREFIX_API_BASQUETE + "/leagues/teams", tags=['leagues'])
async def get_league_name(league_id: Optional[str] = None, league_name: Optional[str] = None):
    if league_id == None and league_name == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='The two query are empty!')
    
    if league_id != None:
        lista_times = listar_times_liga(league_id, 'id')
    elif league_name != None:
        lista_times = listar_times_liga(league_name, 'name')

    if lista_times == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='League not found!')

    lista_json = []

    for item in lista_times:
        item_json = {
            "id": item[0],
            "nome": item[1],
        }

        lista_json.append(item_json)
    
    return lista_json

    
# POST

@router.post(PREFIX_API_BASQUETE + "/leagues", tags=['leagues'])
async def post_league(league: League):
    create = inserir_liga(league)
    
    if create:
        return Response(status_code=status.HTTP_201_CREATED)
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'The team with id {league.id} already exists!')


# PUT

@router.put(PREFIX_API_BASQUETE + '/leagues', tags=['leagues'])
async def put_league(league: League):
    update = upadate_ligas(league)

    if update:
        return league
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=F'League not found!')

# DELETE

@router.delete(PREFIX_API_BASQUETE + '/leagues', tags=['leagues'])
async def del_league(league_id: int):
    deleted = delete(table='ligas_de_basquete', id=league_id)
    
    if deleted:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'league not found!')

