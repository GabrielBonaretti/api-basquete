from typing import List, Optional

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select 

from models.team_model import TeamModel
from schemas.team_schema import TeamSchema
from core.deps import get_session

from utils.request import Request

router = APIRouter()


@router.get("/", response_model=List[TeamSchema])
async def get_teams(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(TeamModel)
        result = await session.execute(query)
        teams: List[TeamModel] = result.scalars().all()
        
        if len(teams) > 0:
            return teams
        else:
            raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are no registered teams!"))


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TeamSchema)
async def post_team(team: TeamSchema, db: AsyncSession = Depends(get_session)):
    new_team = TeamModel(
        league_id = team.league_id,
        name =team.name
    ) 
    
    db.add(new_team)
    await db.commit()
    return new_team


@router.get("/search", status_code=status.HTTP_200_OK, response_model=List[TeamSchema])
async def search_team(team_name: str, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(TeamModel).filter(TeamModel.name.like(f"%{team_name}%"))
        result = await session.execute(query)
        teams: List[TeamModel] = result.scalars().all()
        
        if teams:
            return teams
        else:
            raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="League not found!"))
        

@router.get("/{team_id}", status_code=status.HTTP_200_OK, response_model=TeamSchema)
async def get_team(team_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(TeamModel).filter(TeamModel.id == team_id)
        result = await session.execute(query)
        team = result.scalar_one_or_none()

        if team:
            return team
        else:
            raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="team not found!"))        


@router.put("/{team_id}", status_code=status.HTTP_202_ACCEPTED, response_model=TeamSchema)
async def put_team(team_id: int, team: TeamSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(TeamModel).filter(TeamModel.id == team_id)
        result = await session.execute(query)
        team_update = result.scalar_one_or_none()

        if team_update:
            team_update.league_id = team.league_id
            team_update.name = team.name
            await session.commit()
            return team_update
        else:
            raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="team not found!"))


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(team_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(TeamModel).filter(TeamModel.id == team_id)
        result = await session.execute(query)
        team_delete = result.scalar_one_or_none()
        
        if team_delete:
            await session.delete(team_delete)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="team not found!"))
        
        
@router.get("/teams/analytics/", status_code=status.HTTP_200_OK)
async def get_analytics(team_name: str, season: str, db: AsyncSession = Depends(get_session)):
    '''
    from the "league_name" and "season" parameters. This function takes data from a team in a season. 
    This is done in 3 steps. 
        1st: It checks if the team requested in the parameter is in the json file, if it doesn't have it, it returns 404. 
        2nd: If it does, it consumes a basketball api that returns the id of the league the team plays in and the id of the team researched. 
        3rd: With the information from the previous request, it makes another request to discover the team's data for the specific season.
    Finally, it returns a json with all the team's data.

    *requests are separated into a class, which has the request header as attributes. And there are two methods, one for each request*
    '''

    async with db as session:
        query = select(TeamModel).filter(TeamModel.name.like(f"%{team_name}%"))
        result = await session.execute(query)
        teams: List[TeamSchema] = result.scalars().all()
        
        if not teams:
            raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="team not found!"))       
        
        
        team_name = teams[0].name
        
        params = {"search": team_name}
        
        try:
            # creates the request object
            request_team = Request()

            # returns the request times values
            team = request_team.getTeamInformation(
                endpoint="https://api-basketball.p.rapidapi.com/teams",
                query_string=params
            )

            print(team)
            
            if not team:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='This team dont have analytics!')
            
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
