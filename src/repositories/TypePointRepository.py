from fastapi import Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..tables import TypePoint
from ..database import get_session


class TypePointRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.__session: AsyncSession = session

    async def get(self, id_type: int) -> TypePoint | None:
        entity = await self.__session.get(TypePoint, id_type)
        return entity

    async def get_all(self) -> list[TypePoint]:
        query = select(TypePoint)
        response = await self.__session.execute(query)
        return response.scalars().all()
