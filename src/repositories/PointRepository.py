from datetime import datetime

from fastapi import Depends

from sqlalchemy import select, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession

from ..tables import Point
from ..database import get_session


class PointRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.__session: AsyncSession = session

    async def add(self, point_data: Point):
        try:
            self.__session.add(point_data)
            await self.__session.commit()
        except:
            await self.__session.rollback()
            raise Exception

    async def list_point_in_data_all(self, date: datetime, id_user: int) -> list[Point]:
        query = select(Point).where(and_(
            Point.id_user == id_user,
            Point.datareg == date
        ))
        request = await self.__session.execute(query)
        return request.scalars().all()

    async def list_point_in_data_type(self, date: datetime, id_user: int, type_point: int) -> list[Point]:
        query = select(Point).where(and_(
            Point.id_user == id_user,
            Point.datareg == date,
            Point.id_type_point == type_point
        ))
        request = await self.__session.execute(query)
        return request.scalars().all()

    async def get_last_points_in_date(self, date: datetime, id_user: int, type_point: int):
        query = select(Point).where(
            and_(
                Point.id_user == id_user,
                Point.datareg == date,
                Point.id_type_point == type_point
            )
        ).order_by(desc(Point.id)).limit(1)
        request = await self.__session.execute(query)
        return request.scalars().first()


