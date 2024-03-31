from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from ..models.Message import Message
from ..models.User import TypeUser
from ..models.User import UserGet

from ..services.LoginServices import get_current_user
from ..services import PointServices


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/type_user/all", response_model=list[TypeUser])
async def get_type_point_all(
        service: PointServices = Depends()
):
    type_point_list = await service.get_type_point_all()
    return type_point_list