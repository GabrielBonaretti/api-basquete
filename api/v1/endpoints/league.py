from typing import List, Optional

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.league_model import LeagueModel
from schemas.league_schema import LeagueSchema
from core.deps import get_session

router = APIRouter()


@router.get("/", response_model=List[LeagueSchema])
async def get_leagues(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(LeagueModel)
        result = await session.execute(query)
        leagues: List[LeagueModel] = result.scalars().all()

        if len(leagues) > 0:
            return leagues
        else:
            raise (HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                   detail="There are no registered leagues!"))


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=LeagueSchema)
async def post_league(league: LeagueSchema, db: AsyncSession = Depends(get_session)):
    new_league = LeagueModel(
        name=league.name
    )

    db.add(new_league)
    await db.commit()
    return new_league


@router.get("/search", response_model=List[LeagueSchema], status_code=status.HTTP_200_OK)
async def search_league(league_name: str, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(LeagueModel).filter(LeagueModel.name.like(f"%{league_name}%"))
        result = await session.execute(query)
        leagues: List[LeagueModel] = result.scalars().all()
        
        if leagues:
            return leagues
        else:
            raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="League not found!"))


@router.get("/{league_id}", response_model=LeagueSchema, status_code=status.HTTP_200_OK)
async def get_league(league_id: int,  db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(LeagueModel).filter(LeagueModel.id == int(league_id))
        result = await session.execute(query)
        league = result.scalar_one_or_none()

        if league:
            return league
        else:
            raise (HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                   detail="League not found!"))


@router.put("/{league_id}", response_model=LeagueSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_league(league_id: int, league: LeagueSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(LeagueModel).filter(LeagueModel.id == league_id)
        result = await session.execute(query)
        league_update = result.scalar_one_or_none()

        if league_update:
            league_update.name = league.name
            await session.commit()
            return league_update
        else:
            raise (HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                   detail="League not found!"))


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_league(league_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(LeagueModel).filter(LeagueModel.id == league_id)
        result = await session.execute(query)
        league_delete = result.scalar_one_or_none()

        if league_delete:
            await session.delete(league_delete)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise (HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                   detail="League not found!"))
