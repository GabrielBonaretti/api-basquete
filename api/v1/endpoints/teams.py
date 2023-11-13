from typing import List, Optional

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select 

from models.team_model import TeamModel
from schemas.team_schema import TeamSchema
from core.deps import get_session

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
        
