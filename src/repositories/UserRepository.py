from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from ..tables import User, TypeUser
from ..database import get_session

from fastapi import Depends

from typing import List


class UserRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.__session: AsyncSession = session

    async def count_row(self) -> int:
        response = select(func.count(User.id))
        result = await self.__session.execute(response)
        return result.scalars().first()

    async def get_user(self, id_user: int) -> User:
        result = await self.__session.get(User, id_user)
        return result

    async def get_list_user_by_user_type(self, start: int, limit: int, type_user: str) -> List[User]:
        if type_user == "all":
            response = select(User)
        elif type_user == "user":
            response = select(User).join(TypeUser).where(TypeUser.name != "admin")
        else:
            response = select(User).where(User.type == 1)

        response = response.offset(start).fetch(limit).order_by(User.id)
        result = await self.__session.execute(response)
        return result.unique().scalars().all()

    async def get_user_by_login(self, login: str) -> User:
        response = select(User).where(User.login == login)
        result = await self.__session.execute(response)
        return result.scalars().first()

    async def add(self, user: User):
        try:
            self.__session.add(user)
            await self.__session.commit()
        except:
            await self.__session.rollback()
            raise Exception

    async def update(self, user: User):
        try:
            self.__session.add(user)
            await self.__session.commit()
        except:
            await self.__session.rollback()
            raise Exception

    async def delete(self, user):
        try:
            await self.__session.delete(user)
            await self.__session.commit()
        except:
            await self.__session.rollback()
            raise Exception

    async def get_by_uuid(self, uuid: str) -> User:
        query = select(User).where(User.uuid == uuid)
        response = await self.__session.execute(query)
        return response.scalars().first()

    async def get_user_by_type(self, name_type_user: str) -> list[User]:
        query = select(User).join(TypeUser).where(TypeUser.name == name_type_user)
        response = await self.__session.execute(query)
        return response.scalars().all()


