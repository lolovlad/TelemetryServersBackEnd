from fastapi import Depends, HTTPException, status
from ..repositories import UserRepository
from ..models.User import UserGet
from ..tables import User


class UserServices:
    def __init__(self,
                 user_repository: UserRepository = Depends()):

        self.__user_repository: UserRepository = user_repository

    async def get_equipment_user(self) -> list[UserGet]:
        entity = await self.__user_repository.get_user_by_type("equipment")
        return [UserGet.model_validate(i, from_attributes=True) for i in entity]
