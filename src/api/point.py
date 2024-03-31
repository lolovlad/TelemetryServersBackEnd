from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from ..models.Message import Message
from ..models.Point import PostPoint, TypePoint, GetPoint, GradeEquipment
from ..models.User import UserGet

from ..services.LoginServices import get_current_user
from ..services import PointServices


router = APIRouter(prefix="/point", tags=["point"])


@router.get("/type_point/all", response_model=list[TypePoint])
async def get_type_point_all(
        service: PointServices = Depends()
):
    type_point_list = await service.get_type_point_all()
    return type_point_list


@router.post("/", responses={
    status.HTTP_201_CREATED: {"model": Message}
})
async def add_point(
        point_data: PostPoint,
        user: UserGet = Depends(get_current_user),
        service: PointServices = Depends()
):
    if user.type.name == "equipment":
        await service.app_point(user.uuid, point_data)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "сохранено"}
        )


@router.get("/one_day/{data}/{uuid_user}", response_model=list[GetPoint])
async def get_list_point(
        data: str,
        uuid_user: str,
        type_point: int = 0,
        user: UserGet = Depends(get_current_user),
        service: PointServices = Depends(),
):
    if user.type.name in ("user", "admin"):
        if type_point == 0:
            point_list = await service.get_list_point_all(data, uuid_user)
        else:
            point_list = await service.get_list_point_type(data, uuid_user, type_point)
        return point_list


@router.get("/grade/one_day/{data}/{uuid_user}", response_model=GradeEquipment)
async def get_grade_equ(
        data: str,
        uuid_user: str,
        list_type_point: str,
        user: UserGet = Depends(get_current_user),
        service: PointServices = Depends(),
):
    if user.type.name in ("user", "admin"):
        point_list = await service.grade_equipment(data, uuid_user, list_type_point)
        return point_list
