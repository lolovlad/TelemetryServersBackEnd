from fastapi import Depends, HTTPException, status
from ..repositories import PointRepository, UserRepository, TypePointRepository
from ..models.Point import PostPoint, TypePoint
from ..tables import Point


class UserServices:
    def __init__(self,
                 user_repository: UserRepository = Depends()):

        self.__user_repository: UserRepository = user_repository

    async def get_type_user_all(self) -> list[TypePoint]:
        entity = await self.__type_point_repository.get_all()
        return [TypePoint.model_validate(i, from_attributes=True) for i in entity]
