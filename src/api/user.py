from fastapi import APIRouter, Depends
from ..models.User import UserGet

from ..services.LoginServices import get_current_user
from ..services import UserServices


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/equipment_user/all", response_model=list[UserGet])
async def get_user_equipment(
        user: UserGet = Depends(get_current_user),
        service: UserServices = Depends()
):
    if user.type.name in ("user", "admin"):
        user_list = await service.get_equipment_user()
        return user_list
